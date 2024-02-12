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

        self._targetPagePort = TargetPagePortFactory().create_ai_guide_target_page_port(javaIp="127.0.0.1",
                                                                                   pythonIp="127.0.0.1",
                                                                                   javaPort=2700, pythonPort=2701,
                                                                                   serverName=self._serverName,
                                                                                   rootUrl=f"http://{self._applicationIp}:{self._applicationPort}/",
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
        self._observation_shape = initiateEnvOutput.get_observation_size()

        self.action_space = gym.spaces.Discrete(
            initiateEnvOutput.get_action_space_size())
        self.observation_space = gym.spaces.Box(low=-numpy.inf,
                                                high=numpy.inf,
                                                shape=self._observation_shape,
                                                dtype=numpy.float32)

        self._targetPagePort.connect()
        self._targetPagePort.wait_for_target_page()
        self._isFirstStep = True

        self._targetFormXPath = ''
        self._formCounts = {}

        self._autController.start_aut_server()

    def step(self, action):
        if self._totalStep > self._pauseTotalStep:
            self._targetPagePort.set_pause_agent(True)
            count = 1
            while self._targetPagePort.get_pause_agent():
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

        if self._autOperator.get_focused_app_element() is None:
            focusElementXpath = ""
        else:
            focusElementXpath = self._autOperator.get_focused_app_element().get_xpath()

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
            executeActionOutput.set_is_done(True)

        self._stepsInformation = "total_step:" + f"{self._totalStep:4}" + \
                                 "\tStep:" + f"{self._stepNumber:2}" + \
                                 "\tEpisode:" + str(self._episodeIndex) + \
                                 "\tAction:" + f"{int(action):2}" + \
                                 "\tReward:" + f"{executeActionOutput.getReward(): 4.3f}" + \
                                 "\tFocusElement: " + str(self._originalObservation).ljust(64) + \
                                 "\tXpath: " + focusElementXpath + \
                                 "\tCodeCoverage:" + \
            str(executeActionOutput.get_code_coverage_dict())
        self._logger.info(self._stepsInformation)

        observation = numpy.array(executeActionOutput.get_observation())
        observation.resize(self._observation_shape)
        self._episodeReward += executeActionOutput.get_reward()
        self._stepNumber += 1
        self._totalStep += 1

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

        isLegalDirective = False
        if not self._isFirstStep:
            episodeHandlerEntity = self._episodeHandlerRepository.find_by_id(
                id=self._episodeHandlerId)
            episodeHandler = EpisodeHandlerEntityMapper.mapping_episode_handler_form(
                episodeHandlerEntity)
            states = episodeHandler.get_all_state()
            if states[-2].get_action_type() == "click" and states[-2].get_interacted_element():
                interactiveAppElement: AppElement = states[-2].get_interacted_element(
                )
                tagName = interactiveAppElement.get_tag_name()
                tagType = interactiveAppElement.get_type()
                if tagName == "button" or tagName == "a" or (tagName == 'input' and (
                        tagType == 'submit' or tagType == "button" or tagType == 'image')):
                    afterActionDom = states[-1].get_dom()
                    beforeActionDom = states[-2].get_dom()
                    isLegalDirective = self._directiveRuleService.is_legal(
                        targetPageId=self._targetPageId, beforeActionDom=beforeActionDom, afterActionDom=afterActionDom)

        if isLegalDirective:
            try:
                self._logger.info(
                    f"Find legal directive, target page id: {self._targetPageId}")
                self._logger.info(
                    f"Number of attempts: {self._formCounts[self._targetPageId]}")
                self._targetPagePort.push_target_page(targetPageId=self._targetPageId,
                                                    episodeHandlerId=self._episodeHandlerId)
            except Exception as ex:
                template = 'An exception of type {0} occurred. Arguments:\n{1!r}'
                message = template.format(type(ex).__name__, ex.args)
                self._logger.info(message)
                self._logger.info(f"PUSH ERROR!!! {self._crawler.getUrl()}")

        self._targetPagePort.pull_target_page()

        self._logger.info(
            "\n\n=======================Reset environment.Env=======================")
        self._episodeIndex += 1
        self._stepNumber = 1

        self._autController.reset_aut_server(isLegalDirective)
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
            self._autController.reset_aut_server(True)
            resetEnvUseCase.execute(
                input=resetEnvUseInput,
                output=resetEnvUseOutput)

        self._episodeHandlerId = resetEnvUseOutput.get_episode_handler_id()
        self._targetPageId = resetEnvUseOutput.get_target_page_id()
        self._originalObservation = resetEnvUseOutput.get_original_observation()

        if self._targetPageId in self._formCounts:
            self._formCounts[self._targetPageId] += 1
        else:
            self._formCounts[self._targetPageId] = 1

        self._logger.info("Episode Handler Amount:" +
                          f"{len(self._episodeHandlerRepository.findAll()):2}")
        self._logger.info("Target page id is: " + self._targetPageId)
        self._logger.info(
            "==========================================================\n\n")

        self._targetFormXPath = resetEnvUseOutput.get_form_x_path()

        FormSubmitCriteriaSingleton.get_instance().set_form_submit_criteria(
            applicationName=self._serverName,
            url=resetEnvUseOutput.get_target_page_url(),
            xpath=self._targetFormXPath)

        observation = numpy.array(resetEnvUseOutput.get_observation())
        observation.resize(self._observation_shape)

        self._originalObservation = self._strip_dictionary_contents(
            self._originalObservation)
        self._update_target_page()
        self._isFirstStep = True
        return observation

    def close(self):
        self._autController.stop_aut_server()
        self._crawler.close()
        self._targetPagePort.close()
        self._logger.info(f"form counts: {self._formCounts}")
        self._logger.info("close environment.Env")

    def render(self):
        pass

    def _strip_dictionary_contents(self, dictionary: dict):
        for key in dictionary:
            dictionary[key] = str(dictionary[key]).strip()

        return dictionary

    def _update_target_page(self):
        codeCoverageDTO = self._get_code_coverage_by_type(
            codeCoverageDTOs=self._codeCoverageCollector.get_code_coverage_dt_os(), codeCoverageType=self._codeCoverageType)
        updateTargetPageInput = UpdateTargetPageInput.UpdateTargetPageInput(targetPageId=self._targetPageId,
                                                                            basicCodeCoverageDTO=codeCoverageDTO)
        updateTargetPageOutput = UpdateTargetPageOutput.UpdateTargetPageOutput()
        updateTargetPageUseCase = UpdateTargetPageUseCase.UpdateTargetPageUseCase()
        updateTargetPageUseCase.execute(
            input=updateTargetPageInput,
            output=updateTargetPageOutput)

    def _get_code_coverage_by_type(self, codeCoverageDTOs: [
                               CodeCoverageDTO], codeCoverageType: str):
        for codeCoverageDTO in codeCoverageDTOs:
            if codeCoverageDTO.get_code_coverage_type() == codeCoverageType:
                return codeCoverageDTO

    def get_aut_operator(self):
        return self._autOperator
