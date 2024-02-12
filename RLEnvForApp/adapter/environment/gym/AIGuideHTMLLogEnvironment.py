import gym
import numpy
from dependency_injector.wiring import Provide, inject

from configuration.di.EnvironmentDIContainers import EnvironmentDIContainers
from RLEnvForApp.adapter.environment.autOperator.crawler.HTMLLogCrawler import \
    HTMLLogCrawler
from RLEnvForApp.adapter.targetPagePort.factory.TargetPagePortFactory import \
    TargetPagePortFactory
from RLEnvForApp.logger.logger import Logger
from RLEnvForApp.usecase.environment.autOperator.AIGUIDEOperator import \
    AIGUIDEOperator
from RLEnvForApp.usecase.environment.executeAction import (
    ExecuteActionInput, ExecuteActionOutput, ExecuteActionUseCase)
from RLEnvForApp.usecase.environment.initiateEnvironment import (
    InitiateEnvironmentInput, InitiateEnvironmentOutput,
    InitiateEnvironmentUseCase)
from RLEnvForApp.usecase.environment.resetEnvironment import (
    ResetEnvironmentInput, ResetEnvironmentOutput, ResetEnvironmentUseCase)
from RLEnvForApp.usecase.repository.EpisodeHandlerRepository import \
    EpisodeHandlerRepository


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

        self._targetPagePort = TargetPagePortFactory().create_ai_guide_html_log_target_page_port(
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
        initiateEnvUseCase.execute(
            input=initiateEnvInput,
            output=initiateEnvOutput)

        self._observation_shape = initiateEnvOutput.get_observation_size()

        self.action_space = gym.spaces.Discrete(
            initiateEnvOutput.get_action_space_size())
        self.observation_space = gym.spaces.Box(low=-numpy.inf,
                                                high=numpy.inf,
                                                shape=self._observation_shape,
                                                dtype=numpy.float32)

        self._targetPagePort.connect()
        self._targetPagePort.wait_for_target_page()

    def step(self, action):
        if self._autOperator.get_focused_app_element() is None:
            focusElementXpath = ""
        else:
            focusElementXpath = self._autOperator.get_focused_app_element().get_xpath()

        executeActionUseCase = ExecuteActionUseCase.ExecuteActionUseCase(
            autOperator=self._autOperator)
        executeActionInput = ExecuteActionInput.ExecuteActionInput(actionNumber=int(action),
                                                                   episodeHandlerId=self._episodeHandlerId)
        executeActionOutput = ExecuteActionOutput.ExecuteActionOutput()
        executeActionUseCase.execute(
            input=executeActionInput,
            output=executeActionOutput)

        self._stepsInformation = "total_step:" + f"{self._totalStep:4}" + \
                                 "\tStep:" + f"{self._stepNumber:2}" + \
                                 "\tEpisode:" + str(self._episodeIndex) + \
                                 "\tAction:" + f"{int(action):2}" + \
                                 "\tReward:" + f"{executeActionOutput.getReward(): 4.3f}" + \
                                 "\tFocusElement: " + str(self._originalObservation).ljust(64) + \
                                 "\tXpath: " + focusElementXpath + \
                                 "\tCodeCoverage:" + \
            str(executeActionOutput.get_code_coverage_dict())
        observation = numpy.array(executeActionOutput.get_observation())
        observation.resize(self._observation_shape)
        self._episodeReward += executeActionOutput.get_reward()
        self._stepNumber += 1
        self._totalStep += 1

        self._logger.info(self._stepsInformation)

        self._originalObservation = executeActionOutput.get_original_observation()
        self._originalObservation = self._strip_dictionary_contents(
            self._originalObservation)
        return observation, executeActionOutput.get_reward(), executeActionOutput.get_is_done(), {
            "Reward": executeActionOutput.get_reward()}

    def reset(self):
        self._logger.info(
            "Episode reward:" +
            f"{self._episodeReward:3}")
        self._stepsInformation = ""
        self._episodeReward = 0

        self._logger.info(
            "\n\n=======================Reset environment.Env=======================")
        self._episodeIndex += 1
        self._stepNumber = 1

        resetEnvUseCase = ResetEnvironmentUseCase.ResetEnvironmentUseCase(
            operator=self._autOperator)
        resetEnvUseInput = ResetEnvironmentInput.ResetEnvironmentInput(
            episodeIndex=self._episodeIndex)
        resetEnvUseOutput = ResetEnvironmentOutput.ResetEnvironmentOutput()
        resetEnvUseCase.execute(
            input=resetEnvUseInput,
            output=resetEnvUseOutput)

        self._logger.info("Episode Handler Amount:" +
                          f"{len(self._episodeHandlerRepository.findAll()):2}")
        self._logger.info(
            "Target page url is: " +
            resetEnvUseOutput.get_target_page_url())
        self._logger.info(
            "==========================================================\n\n")

        self._episodeHandlerId = resetEnvUseOutput.get_episode_handler_id()
        self._targetPageId = resetEnvUseOutput.get_target_page_id()
        observation = numpy.array(resetEnvUseOutput.get_observation())
        observation.resize(self._observation_shape)

        self._originalObservation = resetEnvUseOutput.get_original_observation()
        self._originalObservation = self._strip_dictionary_contents(
            self._originalObservation)
        return observation

    def close(self):
        self._crawler.close()
        self._logger.info("close environment.Env")

    def render(self):
        pass

    def _strip_dictionary_contents(self, dictionary: dict):
        for key in dictionary:
            dictionary[key] = str(dictionary[key]).strip()

        return dictionary
