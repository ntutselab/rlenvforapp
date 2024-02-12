import gym
import numpy
import json
import os

from collections import defaultdict
from dependency_injector.wiring import Provide, inject
from RLEnvForApp.adapter.environment.autOperator.crawler.HTMLLogCrawler import HTMLLogCrawler
from RLEnvForApp.adapter.targetPagePort.factory.TargetPagePortFactory import TargetPagePortFactory
from RLEnvForApp.usecase.environment.autOperator.AIGUIDEOperator import AIGUIDEOperator
from RLEnvForApp.usecase.environment.executeAction import *
from RLEnvForApp.usecase.environment.initiateEnvironment import *
from RLEnvForApp.usecase.environment.resetEnvironment import *
from RLEnvForApp.usecase.repository.EpisodeHandlerRepository import EpisodeHandlerRepository
from RLEnvForApp.domain.environment.inputSpace import ValueWeightSingleton, inputTypes, inputValues, CategoryListSingleton
from configuration.di.EnvironmentDIContainers import EnvironmentDIContainers
from RLEnvForApp.logger.logger import Logger


class AIGuideHTMLLogEnvironment(gym.Env):
    @inject
    def __init__(
            self, episodeHandlerRepository: EpisodeHandlerRepository = Provide[EnvironmentDIContainers.episodeHandlerRepository]):
        self._logger = Logger()
        self._logger.info('Init environment.Env')
        self._applicationIp = "127.0.0.1"
        self._applicationPort = 3100

        self._episodeHandlerRepository = episodeHandlerRepository

        self._crawler = HTMLLogCrawler()
        self._autOperator = AIGUIDEOperator(crawler=self._crawler)

        self._targetPagePort = TargetPagePortFactory().createAIGuideHTMLLogTargetPagePort(
            folderPath="htmlSet/GUIDE_HTML_SET")

        self._targetPageId = ""
        self._episodeHandlerId = ""
        self._episodeIndex = 0
        self._stepNumber = 1
        self._totalStep = 1
        self._episodeReward = 0
        self._stepsInformation = ""
        self._originalObservation = {}

        initiateEnvUseCase = InitiateEnvironmentUseCase.InitiateEnvironmentUseCase()
        initiateEnvInput = InitiateEnvironmentInput.InitiateEnvironmentInput()
        initiateEnvOutput = InitiateEnvironmentOutput.InitiateEnvironmentOutput()
        initiateEnvUseCase.execute(input=initiateEnvInput, output=initiateEnvOutput)

        self._observation_shape = initiateEnvOutput.getObservationSize()

        self.action_space = gym.spaces.Discrete(initiateEnvOutput.getActionSpaceSize())
        self.observation_space = gym.spaces.Box(low=-numpy.inf,
                                                high=numpy.inf,
                                                shape=self._observation_shape,
                                                dtype=numpy.float32)

        self._targetPagePort.connect()
        self._targetPagePort.waitForTargetPage()

    def step(self, action):
        if self._autOperator.getFocusedAppElement() is None:
            focusElementXpath = ""
        else:
            focusElementXpath = self._autOperator.getFocusedAppElement().getXpath()

        executeActionUseCase = ExecuteActionUseCase.ExecuteActionUseCase(
            autOperator=self._autOperator)
        executeActionInput = ExecuteActionInput.ExecuteActionInput(actionNumber=int(action),
                                                                   episodeHandlerId=self._episodeHandlerId)
        executeActionOutput = ExecuteActionOutput.ExecuteActionOutput()
        executeActionUseCase.execute(input=executeActionInput, output=executeActionOutput)

        self._stepsInformation = "total_step:" + "{:4}".format(self._totalStep) + \
                                 "\tStep:" + "{:2}".format(self._stepNumber) + \
                                 "\tEpisode:" + str(self._episodeIndex) + \
                                 "\tAction:" + "{:2}".format(int(action)) + \
                                 "\tReward:" + "{: 4.3f}".format(executeActionOutput.getReward()) + \
                                 "\tFocusElement: " + str(self._originalObservation).ljust(64) + \
                                 "\tXpath: " + focusElementXpath + \
                                 "\tCodeCoverage:" + str(executeActionOutput.getCodeCoverageDict())
        observation = numpy.array(executeActionOutput.getObservation())
        observation.resize(self._observation_shape)
        self._episodeReward += executeActionOutput.getReward()
        self._stepNumber += 1
        self._totalStep += 1

        self._logger.info(self._stepsInformation)

        self._originalObservation = executeActionOutput.getOriginalObservation()
        self._originalObservation = self._stripDictionaryContents(self._originalObservation)
        return observation, executeActionOutput.getReward(), executeActionOutput.getIsDone(), {
            "Reward": executeActionOutput.getReward()}

    def reset(self):
        self._logger.info("Episode reward:" + "{:3}".format(self._episodeReward))
        self._stepsInformation = ""
        self._episodeReward = 0

        self._logger.info("\n\n=======================Reset environment.Env=======================")
        self._episodeIndex += 1
        self._stepNumber = 1

        resetEnvUseCase = ResetEnvironmentUseCase.ResetEnvironmentUseCase(
            operator=self._autOperator)
        resetEnvUseInput = ResetEnvironmentInput.ResetEnvironmentInput(
            episodeIndex=self._episodeIndex)
        resetEnvUseOutput = ResetEnvironmentOutput.ResetEnvironmentOutput()
        resetEnvUseCase.execute(input=resetEnvUseInput, output=resetEnvUseOutput)

        self._logger.info("Episode Handler Amount:" +
                          "{:2}".format(len(self._episodeHandlerRepository.findAll())))
        self._logger.info("Target page url is: " + resetEnvUseOutput.getTargetPageUrl())
        self._logger.info("==========================================================\n\n")

        self._episodeHandlerId = resetEnvUseOutput.getEpisodeHandlerId()
        self._targetPageId = resetEnvUseOutput.getTargetPageId()
        observation = numpy.array(resetEnvUseOutput.getObservation())
        observation.resize(self._observation_shape)

        self._originalObservation = resetEnvUseOutput.getOriginalObservation()
        self._originalObservation = self._stripDictionaryContents(self._originalObservation)
        return observation

    def close(self):
        self._crawler.close()
        self._logger.info("close environment.Env")

    def render(self):
        pass

    def _stripDictionaryContents(self, dictionary: dict):
        for key in dictionary:
            dictionary[key] = str(dictionary[key]).strip()

        return dictionary
