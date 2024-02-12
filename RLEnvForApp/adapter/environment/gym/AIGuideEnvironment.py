import time
import traceback

import gym
import numpy
from dependency_injector.wiring import Provide, inject

from configuration.di.EnvironmentDIContainers import EnvironmentDIContainers
from RLEnvForApp.adapter.controller.ApplicationUnderTestController import \
    ApplicationUnderTestController
from RLEnvForApp.adapter.environment.autOperator.codeCoverageCollector.NoCodeCoverageCollector import \
    NoCodeCoverageCollector
from RLEnvForApp.adapter.environment.autOperator.crawler.SeleniumCrawler import \
    SeleniumCrawler
from RLEnvForApp.adapter.targetPagePort.factory.TargetPagePortFactory import \
    TargetPagePortFactory
from RLEnvForApp.domain.environment.state.AppElement import AppElement
from RLEnvForApp.domain.targetPage.DirectiveRuleService.FormSubmitCriteriaSingleton import \
    FormSubmitCriteriaSingleton
from RLEnvForApp.domain.targetPage.DirectiveRuleService.IDirectiveRuleService import \
    IDirectiveRuleService
from RLEnvForApp.logger.logger import Logger
from RLEnvForApp.usecase.environment.autOperator.AIGUIDEOperator import \
    AIGUIDEOperator
from RLEnvForApp.usecase.environment.autOperator.codeCoverageCollector.ICodeCoverageCollector import \
    ICodeCoverageCollector
from RLEnvForApp.usecase.environment.autOperator.dto.CodeCoverageDTO import \
    CodeCoverageDTO
from RLEnvForApp.usecase.environment.episodeHandler.mapper import \
    EpisodeHandlerEntityMapper
from RLEnvForApp.usecase.environment.executeAction import (
    ExecuteActionInput, ExecuteActionOutput, ExecuteActionUseCase)
from RLEnvForApp.usecase.environment.initiateEnvironment import (
    InitiateEnvironmentInput, InitiateEnvironmentOutput,
    InitiateEnvironmentUseCase)
from RLEnvForApp.usecase.environment.resetEnvironment import (
    ResetEnvironmentInput, ResetEnvironmentOutput, ResetEnvironmentUseCase)
from RLEnvForApp.usecase.repository.EpisodeHandlerRepository import \
    EpisodeHandlerRepository
from RLEnvForApp.usecase.targetPage.update import (UpdateTargetPageInput,
                                                   UpdateTargetPageOutput,
                                                   UpdateTargetPageUseCase)


class AIGuideEnvironment(gym.Env):
    @inject
    def __init__(self,
                 episodeHandlerRepository: EpisodeHandlerRepository = Provide[
                     EnvironmentDIContainers.episodeHandlerRepository],
                 directiveRuleService: IDirectiveRuleService = Provide[EnvironmentDIContainers.directiveRuleService]):
        self._logger = Logger()
        self._logger.info("Init environment.Env")
        self._applicationIp = "127.0.0.1"
        self._applicationPort = 3100
        self._codeCoverageType = "statement coverage"

        # self._serverName = "keystonejs_with_coverage"
        self._serverName = "timeoff_management_with_coverage"
        # self._serverName = "nodebb_with_coverage"
        # self._serverName = "django_blog_with_no_coverage"
        # self._serverName = "spring_petclinic_with_no_coverage"
        # self._serverName = "kimai"
        # self._serverName = "oscar"
        # self._serverName = "astuto"
        # self._serverName = "svelte_commerce"

        self._episodeHandlerRepository = episodeHandlerRepository
        self._directiveRuleService: IDirectiveRuleService = directiveRuleService

        self._autController = ApplicationUnderTestController(applicationName=self._serverName,
                                                             serverIP=self._applicationIp, port=self._applicationPort)

        self._crawler = SeleniumCrawler(browserName="Chrome")
        # self._codeCoverageCollector: ICodeCoverageCollector = IstanbulMiddlewareCodeCoverageCollector(
        #     serverIp=self._applicationIp, serverPort=self._applicationPort)
        self._codeCoverageCollector: ICodeCoverageCollector = NoCodeCoverageCollector()
        self._autOperator = AIGUIDEOperator(
            crawler=self._crawler,
            codeCoverageCollector=self._codeCoverageCollector)

        self._targetPagePort = TargetPagePortFactory().createAIGuideTargetPagePort(javaIp="127.0.0.1",
                                                                                   pythonIp="127.0.0.1",
                                                                                   javaPort=2700, pythonPort=2701,
                                                                                   serverName=self._serverName,
                                                                                   rootUrl="http://{ip}:{port}/".format(
                                                                                       ip=self._applicationIp,
                                                                                       port=self._applicationPort),
                                                                                   codeCoverageType=self._codeCoverageType)

        # self._targetPagePort = TargetPagePortFactory().createAIGuideVerifyTargetPagePort(javaIp="127.0.0.1",
        #                                                                            pythonIp="127.0.0.1",
        #                                                                            javaPort=2700, pythonPort=2701,
        #                                                                            serverName=self._serverName,
        #                                                                            rootUrl="http://{ip}:{port}/".format(
        #                                                                                ip=self._applicationIp,
        #                                                                                port=self._applicationPort),
        # codeCoverageType=self._codeCoverageType)

        self._targetPageId = ""
        self._episodeHandlerId = ""
        self._episodeIndex = 0
        self._stepNumber = 1
        self._totalStep = 1
        self._episodeReward = 0
        self._stepsInformation = ""
        self._originalObservation = {}
        # The _pauseInterval represents how many steps the agent will stop and
        # let the crawler play
        self._pauseInterval = 2000
        self._pauseTotalStep = self._pauseInterval

        initiateEnvUseCase = InitiateEnvironmentUseCase.InitiateEnvironmentUseCase()
        initiateEnvInput = InitiateEnvironmentInput.InitiateEnvironmentInput()
        initiateEnvOutput = InitiateEnvironmentOutput.InitiateEnvironmentOutput()
        initiateEnvUseCase.execute(
            input=initiateEnvInput,
            output=initiateEnvOutput)

        self._logger.info(f"Action List: {initiateEnvOutput.getActionList()}")
        self._observation_shape = initiateEnvOutput.getObservationSize()

        self.action_space = gym.spaces.Discrete(
            initiateEnvOutput.getActionSpaceSize())
        self.observation_space = gym.spaces.Box(low=-numpy.inf,
                                                high=numpy.inf,
                                                shape=self._observation_shape,
                                                dtype=numpy.float32)

        self._targetPagePort.connect()
        self._targetPagePort.waitForTargetPage()
        self._isFirstStep = True

        self._targetFormXPath = ''
        self._formCounts = {}

        self._autController.startAUTServer()

    def step(self, action):
        if self._totalStep > self._pauseTotalStep:
            self._targetPagePort.setPauseAgent(True)
            count = 1
            while self._targetPagePort.getPauseAgent():
                time.sleep(60)
                self._logger.info(f'sleep count: {count}')
                count += 1
            self._pauseTotalStep += self._pauseInterval

        if self._isFirstStep:
            self._logger.info("In first step.")
            # episodeHandlerEntity = self._episodeHandlerRepository.findById(id=self._episodeHandlerId)
            # episodeHandler = EpisodeHandlerEntityMapper.mappingEpisodeHandlerForm(episodeHandlerEntity=episodeHandlerEntity)
            # episodeHandler.setAllState([self._autOperator.getState()])
            # episodeHandlerEntity = EpisodeHandlerEntityMapper.mappingEpisodeHandlerEntityForm(episodeHandler=episodeHandler)
            # self._episodeHandlerRepository.update(episodeHandlerEntity)
            self._isFirstStep = False

        if self._autOperator.getFocusedAppElement() is None:
            focusElementXpath = ""
        else:
            focusElementXpath = self._autOperator.getFocusedAppElement().getXpath()

        executeActionUseCase = ExecuteActionUseCase.ExecuteActionUseCase(
            autOperator=self._autOperator)
        executeActionInput = ExecuteActionInput.ExecuteActionInput(
            actionNumber=int(action), episodeHandlerId=self._episodeHandlerId)
        executeActionOutput = ExecuteActionOutput.ExecuteActionOutput()

        try:
            executeActionUseCase.execute(
                input=executeActionInput,
                output=executeActionOutput)
        except Exception as e:
            self._logger.exception(f"Something wrong when execute action: {e}")
            traceback.print_exc()
            executeActionOutput.setIsDone(True)

        self._stepsInformation = "total_step:" + "{:4}".format(self._totalStep) + \
                                 "\tStep:" + "{:2}".format(self._stepNumber) + \
                                 "\tEpisode:" + str(self._episodeIndex) + \
                                 "\tAction:" + "{:2}".format(int(action)) + \
                                 "\tReward:" + "{: 4.3f}".format(executeActionOutput.getReward()) + \
                                 "\tFocusElement: " + str(self._originalObservation).ljust(64) + \
                                 "\tXpath: " + focusElementXpath + \
                                 "\tCodeCoverage:" + \
            str(executeActionOutput.getCodeCoverageDict())
        self._logger.info(self._stepsInformation)

        observation = numpy.array(executeActionOutput.getObservation())
        observation.resize(self._observation_shape)
        self._episodeReward += executeActionOutput.getReward()
        self._stepNumber += 1
        self._totalStep += 1

        self._originalObservation = executeActionOutput.getOriginalObservation()
        self._originalObservation = self._stripDictionaryContents(
            self._originalObservation)
        return observation, executeActionOutput.getReward(), executeActionOutput.getIsDone(), {
            "Reward": executeActionOutput.getReward()}

    def reset(self):
        self._logger.info(
            "Episode reward:" +
            "{:3}".format(
                self._episodeReward))
        self._stepsInformation = ""
        self._episodeReward = 0

        isLegalDirective = False
        if not self._isFirstStep:
            episodeHandlerEntity = self._episodeHandlerRepository.findById(
                id=self._episodeHandlerId)
            episodeHandler = EpisodeHandlerEntityMapper.mappingEpisodeHandlerForm(
                episodeHandlerEntity)
            states = episodeHandler.getAllState()
            if states[-2].getActionType() == "click" and states[-2].getInteractedElement():
                interactiveAppElement: AppElement = states[-2].getInteractedElement(
                )
                tagName = interactiveAppElement.getTagName()
                tagType = interactiveAppElement.getType()
                if tagName == "button" or tagName == "a" or (tagName == 'input' and (
                        tagType == 'submit' or tagType == "button" or tagType == 'image')):
                    afterActionDom = states[-1].getDOM()
                    beforeActionDom = states[-2].getDOM()
                    isLegalDirective = self._directiveRuleService.isLegal(
                        targetPageId=self._targetPageId, beforeActionDom=beforeActionDom, afterActionDom=afterActionDom)

        if isLegalDirective:
            try:
                self._logger.info(
                    f"Find legal directive, target page id: {self._targetPageId}")
                self._logger.info(
                    f"Number of attempts: {self._formCounts[self._targetPageId]}")
                self._targetPagePort.pushTargetPage(targetPageId=self._targetPageId,
                                                    episodeHandlerId=self._episodeHandlerId)
            except Exception as ex:
                template = 'An exception of type {0} occurred. Arguments:\n{1!r}'
                message = template.format(type(ex).__name__, ex.args)
                self._logger.info(message)
                self._logger.info(f"PUSH ERROR!!! {self._crawler.getUrl()}")

        self._targetPagePort.pullTargetPage()

        self._logger.info(
            "\n\n=======================Reset environment.Env=======================")
        self._episodeIndex += 1
        self._stepNumber = 1

        self._autController.resetAUTServer(isLegalDirective)
        resetEnvUseCase = ResetEnvironmentUseCase.ResetEnvironmentUseCase(
            operator=self._autOperator)
        resetEnvUseInput = ResetEnvironmentInput.ResetEnvironmentInput(
            episodeIndex=self._episodeIndex)
        resetEnvUseOutput = ResetEnvironmentOutput.ResetEnvironmentOutput()
        try:
            resetEnvUseCase.execute(
                input=resetEnvUseInput,
                output=resetEnvUseOutput)
        except RuntimeError:
            self._autController.resetAUTServer(True)
            resetEnvUseCase.execute(
                input=resetEnvUseInput,
                output=resetEnvUseOutput)

        self._episodeHandlerId = resetEnvUseOutput.getEpisodeHandlerId()
        self._targetPageId = resetEnvUseOutput.getTargetPageId()
        self._originalObservation = resetEnvUseOutput.getOriginalObservation()

        if self._targetPageId in self._formCounts:
            self._formCounts[self._targetPageId] += 1
        else:
            self._formCounts[self._targetPageId] = 1

        self._logger.info("Episode Handler Amount:" +
                          "{:2}".format(len(self._episodeHandlerRepository.findAll())))
        self._logger.info("Target page id is: " + self._targetPageId)
        self._logger.info(
            "==========================================================\n\n")

        self._targetFormXPath = resetEnvUseOutput.getFormXPath()

        FormSubmitCriteriaSingleton.getInstance().setFormSubmitCriteria(
            applicationName=self._serverName,
            url=resetEnvUseOutput.getTargetPageUrl(),
            xpath=self._targetFormXPath)

        observation = numpy.array(resetEnvUseOutput.getObservation())
        observation.resize(self._observation_shape)

        self._originalObservation = self._stripDictionaryContents(
            self._originalObservation)
        self._updateTargetPage()
        self._isFirstStep = True
        return observation

    def close(self):
        self._autController.stopAUTServer()
        self._crawler.close()
        self._targetPagePort.close()
        self._logger.info(f"form counts: {self._formCounts}")
        self._logger.info("close environment.Env")

    def render(self):
        pass

    def _stripDictionaryContents(self, dictionary: dict):
        for key in dictionary:
            dictionary[key] = str(dictionary[key]).strip()

        return dictionary

    def _updateTargetPage(self):
        codeCoverageDTO = self._getCodeCoverageByType(
            codeCoverageDTOs=self._codeCoverageCollector.getCodeCoverageDTOs(), codeCoverageType=self._codeCoverageType)
        updateTargetPageInput = UpdateTargetPageInput.UpdateTargetPageInput(targetPageId=self._targetPageId,
                                                                            basicCodeCoverageDTO=codeCoverageDTO)
        updateTargetPageOutput = UpdateTargetPageOutput.UpdateTargetPageOutput()
        updateTargetPageUseCase = UpdateTargetPageUseCase.UpdateTargetPageUseCase()
        updateTargetPageUseCase.execute(
            input=updateTargetPageInput,
            output=updateTargetPageOutput)

    def _getCodeCoverageByType(self, codeCoverageDTOs: [
                               CodeCoverageDTO], codeCoverageType: str):
        for codeCoverageDTO in codeCoverageDTOs:
            if codeCoverageDTO.getCodeCoverageType() == codeCoverageType:
                return codeCoverageDTO

    def getAUTOperator(self):
        return self._autOperator
