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
        self._application_ip = "127.0.0.1"
        self._application_port = 3100
        self._code_coverage_type = "statement coverage"

        # self._serverName = "keystonejs_with_coverage"
        self._server_name = "timeoff_management_with_coverage"
        # self._serverName = "nodebb_with_coverage"
        # self._serverName = "django_blog_with_no_coverage"
        # self._serverName = "spring_petclinic_with_no_coverage"
        # self._serverName = "kimai"
        # self._serverName = "oscar"
        # self._serverName = "astuto"
        # self._serverName = "svelte_commerce"

        self._episode_handler_repository = episodeHandlerRepository
        self._directive_rule_service: IDirectiveRuleService = directiveRuleService

        self._aut_controller = ApplicationUnderTestController(applicationName=self._server_name,
                                                             serverIP=self._application_ip, port=self._application_port)

        self._crawler = SeleniumCrawler(browser_name="Chrome")
        # self._codeCoverageCollector: ICodeCoverageCollector = IstanbulMiddlewareCodeCoverageCollector(
        #     serverIp=self._applicationIp, serverPort=self._applicationPort)
        self._code_coverage_collector: ICodeCoverageCollector = NoCodeCoverageCollector()
        self._aut_operator = AIGUIDEOperator(
            crawler=self._crawler,
            code_coverage_collector=self._code_coverage_collector)

        self._target_page_port = TargetPagePortFactory().create_ai_guide_target_page_port(javaIp="127.0.0.1",
                                                                                   pythonIp="127.0.0.1",
                                                                                   javaPort=2700, pythonPort=2701,
                                                                                   serverName=self._server_name,
                                                                                   root_url=f"http://{self._applicationIp}:{self._applicationPort}/",
                                                                                   code_coverage_type=self._code_coverage_type)

        # self._targetPagePort = TargetPagePortFactory().createAIGuideVerifyTargetPagePort(javaIp="127.0.0.1",
        #                                                                            pythonIp="127.0.0.1",
        #                                                                            javaPort=2700, pythonPort=2701,
        #                                                                            serverName=self._serverName,
        #                                                                            rootUrl="http://{ip}:{port}/".format(
        #                                                                                ip=self._applicationIp,
        #                                                                                port=self._applicationPort),
        # codeCoverageType=self._codeCoverageType)

        self._target_page_id = ""
        self._episode_handler_id = ""
        self._episode_index = 0
        self._step_number = 1
        self._total_step = 1
        self._episode_reward = 0
        self._steps_information = ""
        self._original_observation = {}
        # The _pauseInterval represents how many steps the agent will stop and
        # let the crawler play
        self._pause_interval = 2000
        self._pause_total_step = self._pause_interval

        initiate_env_use_case = InitiateEnvironmentUseCase.InitiateEnvironmentUseCase()
        initiate_env_input = InitiateEnvironmentInput.InitiateEnvironmentInput()
        initiate_env_output = InitiateEnvironmentOutput.InitiateEnvironmentOutput()
        initiate_env_use_case.execute(
            input=initiate_env_input,
            output=initiate_env_output)

        self._logger.info(f"Action List: {initiateEnvOutput.getActionList()}")
        self._observation_shape = initiate_env_output.get_observation_size()

        self.action_space = gym.spaces.Discrete(
            initiate_env_output.get_action_space_size())
        self.observation_space = gym.spaces.Box(low=-numpy.inf,
                                                high=numpy.inf,
                                                shape=self._observation_shape,
                                                dtype=numpy.float32)

        self._target_page_port.connect()
        self._target_page_port.wait_for_target_page()
        self._is_first_step = True

        self._target_form_xpath = ''
        self._form_counts = {}

        self._aut_controller.start_aut_server()

    def step(self, action):
        if self._total_step > self._pause_total_step:
            self._target_page_port.set_pause_agent(True)
            count = 1
            while self._target_page_port.get_pause_agent():
                time.sleep(60)
                self._logger.info(f'sleep count: {count}')
                count += 1
            self._pause_total_step += self._pause_interval

        if self._is_first_step:
            self._logger.info("In first step.")
            # episodeHandlerEntity = self._episodeHandlerRepository.findById(id=self._episodeHandlerId)
            # episodeHandler = EpisodeHandlerEntityMapper.mappingEpisodeHandlerForm(episodeHandlerEntity=episodeHandlerEntity)
            # episodeHandler.setAllState([self._autOperator.getState()])
            # episodeHandlerEntity = EpisodeHandlerEntityMapper.mappingEpisodeHandlerEntityForm(episodeHandler=episodeHandler)
            # self._episodeHandlerRepository.update(episodeHandlerEntity)
            self._is_first_step = False

        if self._aut_operator.get_focused_app_element() is None:
            focusElementXpath = ""
        else:
            focusElementXpath = self._aut_operator.get_focused_app_element().get_xpath()

        execute_action_use_case = ExecuteActionUseCase.ExecuteActionUseCase(
            aut_operator=self._aut_operator)
        execute_action_input = ExecuteActionInput.ExecuteActionInput(
            actionNumber=int(action), episode_handler_id=self._episode_handler_id)
        execute_action_output = ExecuteActionOutput.ExecuteActionOutput()

        try:
            execute_action_use_case.execute(
                input=execute_action_input,
                output=execute_action_output)
        except Exception as exception:
            self._logger.exception(f"Something wrong when execute action: {exception}")
            traceback.print_exc()
            execute_action_output.set_is_done(True)

        self._steps_information = "total_step:" + f"{self._totalStep:4}" + \
                                 "\tStep:" + f"{self._stepNumber:2}" + \
                                 "\tEpisode:" + str(self._episode_index) + \
                                 "\tAction:" + f"{int(action):2}" + \
                                 "\tReward:" + f"{executeActionOutput.getReward(): 4.3f}" + \
                                 "\tFocusElement: " + str(self._original_observation).ljust(64) + \
                                 "\tXpath: " + focusElementXpath + \
                                 "\tCodeCoverage:" + \
            str(execute_action_output.get_code_coverage_dict())
        self._logger.info(self._steps_information)

        observation = numpy.array(execute_action_output.get_observation())
        observation.resize(self._observation_shape)
        self._episode_reward += execute_action_output.get_reward()
        self._step_number += 1
        self._total_step += 1

        self._original_observation = execute_action_output.get_original_observation()
        self._original_observation = self._strip_dictionary_contents(
            self._original_observation)
        return observation, execute_action_output.get_reward(), execute_action_output.get_is_done(), {
            "Reward": execute_action_output.get_reward()}

    def reset(self):
        self._logger.info(
            "Episode reward:" +
            f"{self._episodeReward:3}")
        self._steps_information = ""
        self._episode_reward = 0

        is_legal_directive = False
        if not self._is_first_step:
            episode_handler_entity = self._episode_handler_repository.find_by_id(
                id=self._episode_handler_id)
            episode_handler = EpisodeHandlerEntityMapper.mapping_episode_handler_form(
                episode_handler_entity)
            states = episode_handler.get_all_state()
            if states[-2].get_action_type() == "click" and states[-2].get_interacted_element():
                interactiveAppElement: AppElement = states[-2].get_interacted_element(
                )
                tag_name = interactiveAppElement.get_tag_name()
                tagType = interactiveAppElement.get_type()
                if tag_name == "button" or tag_name == "a" or (tag_name == 'input' and (
                        tagType == 'submit' or tagType == "button" or tagType == 'image')):
                    afterActionDom = states[-1].get_dom()
                    beforeActionDom = states[-2].get_dom()
                    is_legal_directive = self._directive_rule_service.is_legal(
                        target_page_id=self._target_page_id, beforeActionDom=beforeActionDom, afterActionDom=afterActionDom)

        if is_legal_directive:
            try:
                self._logger.info(
                    f"Find legal directive, target page id: {self._targetPageId}")
                self._logger.info(
                    f"Number of attempts: {self._formCounts[self._targetPageId]}")
                self._target_page_port.push_target_page(target_page_id=self._target_page_id,
                                                    episode_handler_id=self._episode_handler_id)
            except Exception as exception:
                template = 'An exception of type {0} occurred. Arguments:\n{1!r}'
                message = template.format(type(exception).__name__, exception.args)
                self._logger.info(message)
                self._logger.info(f"PUSH ERROR!!! {self._crawler.getUrl()}")

        self._target_page_port.pull_target_page()

        self._logger.info(
            "\n\n=======================Reset environment.Env=======================")
        self._episode_index += 1
        self._step_number = 1

        self._aut_controller.reset_aut_server(is_legal_directive)
        reset_env_use_case = ResetEnvironmentUseCase.ResetEnvironmentUseCase(
            operator=self._aut_operator)
        reset_env_use_input = ResetEnvironmentInput.ResetEnvironmentInput(
            episodeIndex=self._episode_index)
        reset_env_use_output = ResetEnvironmentOutput.ResetEnvironmentOutput()
        try:
            reset_env_use_case.execute(
                input=reset_env_use_input,
                output=reset_env_use_output)
        except RuntimeError:
            self._aut_controller.reset_aut_server(True)
            reset_env_use_case.execute(
                input=reset_env_use_input,
                output=reset_env_use_output)

        self._episode_handler_id = reset_env_use_output.get_episode_handler_id()
        self._target_page_id = reset_env_use_output.get_target_page_id()
        self._original_observation = reset_env_use_output.get_original_observation()

        if self._target_page_id in self._form_counts:
            self._form_counts[self._target_page_id] += 1
        else:
            self._form_counts[self._target_page_id] = 1

        self._logger.info("Episode Handler Amount:" +
                          f"{len(self._episodeHandlerRepository.findAll()):2}")
        self._logger.info("Target page id is: " + self._target_page_id)
        self._logger.info(
            "==========================================================\n\n")

        self._target_form_xpath = reset_env_use_output.get_form_xpath()

        FormSubmitCriteriaSingleton.get_instance().set_form_submit_criteria(
            applicationName=self._server_name,
            url=reset_env_use_output.get_target_page_url(),
            xpath=self._target_form_xpath)

        observation = numpy.array(reset_env_use_output.get_observation())
        observation.resize(self._observation_shape)

        self._original_observation = self._strip_dictionary_contents(
            self._original_observation)
        self._update_target_page()
        self._is_first_step = True
        return observation

    def close(self):
        self._aut_controller.stop_aut_server()
        self._crawler.close()
        self._target_page_port.close()
        self._logger.info(f"form counts: {self._formCounts}")
        self._logger.info("close environment.Env")

    def render(self):
        pass

    def _strip_dictionary_contents(self, dictionary: dict):
        for key in dictionary:
            dictionary[key] = str(dictionary[key]).strip()

        return dictionary

    def _update_target_page(self):
        code_coverage_dto = self._get_code_coverage_by_type(
            code_coverage_dt_os=self._code_coverage_collector.get_code_coverage_dt_os(), code_coverage_type=self._code_coverage_type)
        update_target_page_input = UpdateTargetPageInput.UpdateTargetPageInput(target_page_id=self._target_page_id,
                                                                            basic_code_coverage_dto=code_coverage_dto)
        update_target_page_output = UpdateTargetPageOutput.UpdateTargetPageOutput()
        update_target_page_use_case = UpdateTargetPageUseCase.UpdateTargetPageUseCase()
        update_target_page_use_case.execute(
            input=update_target_page_input,
            output=update_target_page_output)

    def _get_code_coverage_by_type(self, code_coverage_dt_os: [
                               CodeCoverageDTO], code_coverage_type: str):
        for code_coverage_dto in code_coverage_dt_os:
            if code_coverage_dto.get_code_coverage_type() == code_coverage_type:
                return code_coverage_dto

    def get_aut_operator(self):
        return self._aut_operator
