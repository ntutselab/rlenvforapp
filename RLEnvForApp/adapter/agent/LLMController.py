import json
import os
import re
import traceback
from io import StringIO
from urllib.parse import urlparse

import torch
from dependency_injector.wiring import Provide, inject
from lxml import etree
from openprompt.data_utils import InputExample

from RLEnvForApp.adapter.agent.model.builder.PromptModelBuilder import PromptModelBuilder
from RLEnvForApp.adapter.agent.model.builder.PromptModelDirector import PromptModelDirector
from RLEnvForApp.adapter.controller.ApplicationUnderTestController import ApplicationUnderTestController
from RLEnvForApp.adapter.environment.autOperator.codeCoverageCollector.IstanbulMiddlewareCodeCoverageCollector import \
    IstanbulMiddlewareCodeCoverageCollector
from RLEnvForApp.adapter.environment.autOperator.codeCoverageCollector.NoCodeCoverageCollector import \
    NoCodeCoverageCollector
from RLEnvForApp.adapter.environment.autOperator.crawler.SeleniumCrawler import SeleniumCrawler
from RLEnvForApp.adapter.llmService.ChatGPTService import ChatGPTService
from RLEnvForApp.adapter.targetPagePort.FileManager import FileManager
from RLEnvForApp.adapter.targetPagePort.factory.TargetPagePortFactory import TargetPagePortFactory
from RLEnvForApp.domain.environment.actionCommand.InitiateToTargetActionCommand import NosuchElementException
from RLEnvForApp.domain.environment.state.AppElement import AppElement
from RLEnvForApp.domain.environment.state.State import State
from RLEnvForApp.domain.llmService import LlmServiceContainer
from RLEnvForApp.domain.llmService.SystemPromptFactory import SystemPromptFactory
from RLEnvForApp.domain.llmService.ILlmService import ILlmService
from RLEnvForApp.domain.targetPage.DirectiveRuleService.FormSubmitCriteriaSingleton import FormSubmitCriteriaSingleton
from RLEnvForApp.domain.targetPage.DirectiveRuleService.IDirectiveRuleService import IDirectiveRuleService
from RLEnvForApp.logger.logger import Logger
from RLEnvForApp.usecase.environment.autOperator.AIGUIDEOperator import AIGUIDEOperator
from RLEnvForApp.usecase.environment.autOperator.codeCoverageCollector.ICodeCoverageCollector import \
    ICodeCoverageCollector
from RLEnvForApp.usecase.environment.episodeHandler.dto.EpisodeHandlerDTO import EpisodeHandlerDTO
from RLEnvForApp.usecase.environment.episodeHandler.get.GetEpisodeHandlerInput import GetEpisodeHandlerInput
from RLEnvForApp.usecase.environment.episodeHandler.get.GetEpisodeHandlerOutput import GetEpisodeHandlerOutput
from RLEnvForApp.usecase.environment.episodeHandler.get.GetEpisodeHandlerUseCase import GetEpisodeHandlerUseCase
from RLEnvForApp.usecase.environment.episodeHandler.mapper import EpisodeHandlerEntityMapper
from RLEnvForApp.usecase.environment.executeAction.ExecuteActionInput import ExecuteActionInput
from RLEnvForApp.usecase.environment.executeAction.ExecuteActionOutput import ExecuteActionOutput
from RLEnvForApp.usecase.environment.executeAction.ExecuteActionUseCase import ExecuteActionUseCase
from RLEnvForApp.usecase.environment.resetEnvironment.ResetEnvironmentInput import ResetEnvironmentInput
from RLEnvForApp.usecase.environment.resetEnvironment.ResetEnvironmentOutput import ResetEnvironmentOutput
from RLEnvForApp.usecase.environment.resetEnvironment.ResetEnvironmentUseCase import ResetEnvironmentUseCase
from RLEnvForApp.usecase.environment.state.dto.stateDTO import StateDTO
from RLEnvForApp.usecase.repository.EpisodeHandlerRepository import EpisodeHandlerRepository
from RLEnvForApp.usecase.repository.TargetPageRepository import TargetPageRepository
from RLEnvForApp.usecase.targetPage.create.CreateDirectiveInput import CreateDirectiveInput
from RLEnvForApp.usecase.targetPage.create.CreateDirectiveOutput import CreateDirectiveOutput
from RLEnvForApp.usecase.targetPage.create.CreateDirectiveUseCase import CreateDirectiveUseCase
from RLEnvForApp.usecase.targetPage.create.CreateFakeDirectiveUseCase import CreateFakeDirectiveUseCase
from RLEnvForApp.usecase.targetPage.dto.DirectiveDTO import DirectiveDTO
from RLEnvForApp.usecase.targetPage.remove.RemoveTargetPageInput import RemoveTargetPageInput
from RLEnvForApp.usecase.targetPage.remove.RemoveTargetPageOutput import RemoveTargetPageOutput
from RLEnvForApp.usecase.targetPage.remove.RemoveTargetPageUseCase import RemoveTargetPageUseCase
from configuration.di.EnvironmentDIContainers import EnvironmentDIContainers


class LLMController:

    @inject
    def __init__(self,
                 episode_handler_repository: EpisodeHandlerRepository =
                 Provide[EnvironmentDIContainers.episodeHandlerRepository],
                 directive_rule_service: IDirectiveRuleService =
                 Provide[EnvironmentDIContainers.directiveRuleService],
                 repository: TargetPageRepository = Provide[EnvironmentDIContainers.targetPageRepository],
                 llm_service : ILlmService = Provide[EnvironmentDIContainers.llmService],):
        self._llm_service = llm_service
        LlmServiceContainer.llm_service_instance.set_instance(llm_service)

        self._fake_data = {}
        self._episode_handler_id = None
        self._form_counts = {}
        self._directive_rule_service = directive_rule_service
        self._episode_handler_repository = episode_handler_repository
        self._repository = repository
        self.__server_name = "timeoff_management_with_coverage"
        self.__application_ip = "localhost"
        self.__application_port = 3100
        self.__coverage_server_port = 3100
        self.__code_coverage_type = "statement coverage"
        self._logger = Logger()
        self._logger.info("Init LLM.Env")
        self.__aut_controller = ApplicationUnderTestController(applicationName=self.__server_name,
                                                               serverIP=self.__application_ip,
                                                               port=self.__application_port)
        self.__crawler = SeleniumCrawler("Chrome")
        self.__code_coverage_collector: ICodeCoverageCollector = IstanbulMiddlewareCodeCoverageCollector(
            serverIp=self.__application_ip, serverPort=self.__coverage_server_port)
        # self.__code_coverage_collector: ICodeCoverageCollector = NoCodeCoverageCollector()
        self.__aut_operator = AIGUIDEOperator(
            crawler=self.__crawler, codeCoverageCollector=self.__code_coverage_collector)
        self.__target_page_port = TargetPagePortFactory().createAIGuideTargetPagePort(javaIp="127.0.0.1",
                                                                                      pythonIp="127.0.0.1",
                                                                                      javaPort=2700, pythonPort=2701,
                                                                                      serverName=self.__server_name,
                                                                                      rootUrl=f"http://"
                                                                                              f"{self.__application_ip}:"
                                                                                              f"{self.__application_port}/",
                                                                                      codeCoverageType=
                                                                                      self.__code_coverage_type)
        self.__target_page_port.connect()
        self.__target_form_xpath = ''
        self.__form_counts = {}
        self._target_page_id = ""
        self._episodeIndex = 0
        self.__aut_controller.startAUTServer()

        self.prompt_model_builder = PromptModelBuilder()
        self.fake_prompt_model_builder = PromptModelBuilder()
        self.prompt_model = PromptModelDirector().make_my_research(self.prompt_model_builder)
        self.fake_prompt_model = PromptModelDirector().make_fake_prompt_model(self.fake_prompt_model_builder)
        # check cuda
        if torch.cuda.is_available():
            self._logger.info("CUDA is available")
            torch.cuda.empty_cache()
            self.prompt_model = self.prompt_model.cuda()
            self.fake_prompt_model = self.fake_prompt_model.cuda()

    def play(self):
        while True:
            if len(self._repository.findAll()) == 0:
                self.__target_page_port.waitForTargetPage()
            self.__aut_controller.resetAUTServer(True)
            self._episodeIndex += 1
            is_legal_directive = False

            try:
                reset_env_use_output = self._reset_environment()
            except NosuchElementException:
                continue

            FormSubmitCriteriaSingleton.getInstance().setFormSubmitCriteria(applicationName=self.__server_name,
                                                                            url=reset_env_use_output.getTargetPageUrl(),
                                                                            xpath=reset_env_use_output.getFormXPath())
            self._target_page_id = reset_env_use_output.getTargetPageId()
            self._episode_handler_id = reset_env_use_output.getEpisodeHandlerId()
            self.__target_form_xpath = reset_env_use_output.getFormXPath()

            while not is_legal_directive:
                app_element: AppElement = self.__aut_operator.getFocusedAppElement()
                if app_element is None:
                    if len(self.__aut_operator.getAllSelectedAppElements()) == 0:
                        self._remove_target_page()
                    break

                final_submit = self._execute_action(app_element, reset_env_use_output.getTargetPageUrl())

                if self._target_page_id not in self._form_counts:
                    self._form_counts[self._target_page_id] = 1

                if final_submit.getIsDone():
                    is_legal_directive = self._is_legal_directive()

                if final_submit.getIsDone() and is_legal_directive:
                    try:
                        self._logger.info(f"Find legal directive, target page id: {self._target_page_id}")
                        self._logger.info(f"Number of attempts: {self._form_counts[self._target_page_id]}")
                        # directive_dto = self._create_fake_directive(self._target_page_id, self._episode_handler_id)
                        # self.__target_page_port.push_target_page_by_directive(self._target_page_id, directive_dto)
                        self.__target_page_port.pushTargetPage(self._target_page_id, self._episode_handler_id)
                        self._fake_data = {}
                    except Exception as ex:
                        template = 'An exception of type {0} occurred. Arguments:\n{1!r}'
                        message = template.format(type(ex).__name__, ex.args)
                        self._logger.info(message)
                        self._fake_data = {}
                        self._logger.info(f"PUSH ERROR!!! {self.__crawler.getUrl()}")
                elif final_submit.getIsDone() and not is_legal_directive:
                    # TODO: This is a temporary solution by AI, need to be checked by human
                    self._form_counts[self._target_page_id] += 1
                    self._fake_data = {}
                    # clean the state
                    episode_handler_entity = self._episode_handler_repository.findById(self._episode_handler_id)
                    episode_handler = EpisodeHandlerEntityMapper.mappingEpisodeHandlerForm(episode_handler_entity)
                    episode_handler.remain_only_index_zero_state()
                    self._logger.info(f"Find illegal directive, target page id: {self._target_page_id}")
                    self._logger.info(f"Number of attempts: {self._form_counts[self._target_page_id]}")
                    if self._form_counts[self._target_page_id] >= 10:
                        self._form_counts[self._target_page_id] = 0
                        directive_dto = self._create_directive(self._target_page_id, self._episode_handler_id)
                        self._save_target_page_to_html_set(self._episode_handler_id, directive_dto)
                        self._remove_target_page()
                        break

    def _check_is_password(self, app_element: AppElement):
        # check if the element is a password field use regex
        if re.search(r'password', app_element.getName(), re.IGNORECASE) or re.search(r'password', app_element.getLabel(),
                                                                                   re.IGNORECASE) or re.search(
                r'password', app_element.getPlaceholder(), re.IGNORECASE):
            return True
        return False

    def _save_target_page_to_html_set(self, episode_handler_id: str, directive_dto: DirectiveDTO):
        file_name = f"{self.__server_name}_{urlparse(directive_dto.getUrl()).path.replace('/', '_')}_{directive_dto.getFormXPath().replace('/', '_')}"
        initial_state_dto: StateDTO = self._get_episode_handler_dto(
            episode_handler_id=episode_handler_id).getStateDTOs()[0]

        interactive_app_element_dictionary = []
        directive_dictionary = {}
        for app_event_dto in directive_dto.getAppEventDTOs():
            directive_dictionary[app_event_dto.getXpath()] = {
                "value": app_event_dto.getValue(), "category": app_event_dto.getCategory()}
        for app_element_dto in initial_state_dto.getSelectedAppElementDTOs():
            interactive_app_element_dictionary.append(app_element_dto.getXpath())
        form_x_path = directive_dto.getFormXPath()
        directive_log_json = json.dumps({"interactive_appElement": interactive_app_element_dictionary,
                                         "appEvent": directive_dictionary, "formXPath": form_x_path})

        # self._updateInputValueWeights(directiveDictionary)

        Logger().info(f"Save html set:\n{file_name}\n{form_x_path}\n{directive_dictionary}")

        file_manager = FileManager()
        file_manager.createFolder("htmlSet", "FAILED_HTML_SET")
        file_manager.createFile(path=os.path.join("htmlSet", "FAILED_HTML_SET"),
                                fileName=file_name + ".html", context=directive_dto.getDom())
        file_manager.createFile(path=os.path.join("htmlSet", "FAILED_HTML_SET"),
                                fileName=file_name + ".json", context=directive_log_json)

    def _create_directive(self, target_page_id: str, episode_handler_id: str):
        create_directive_use_case = CreateDirectiveUseCase()
        create_directive_input = CreateDirectiveInput(targetPageId=target_page_id, episodeHandlerId=episode_handler_id)
        create_directive_output = CreateDirectiveOutput()
        create_directive_use_case.execute(create_directive_input, create_directive_output)
        return create_directive_output.getDirectiveDTO()

    def _create_fake_directive(self, target_page_id: str, episode_handler_id: str):
        create_directive_use_case = CreateFakeDirectiveUseCase()
        create_directive_input = CreateDirectiveInput(targetPageId=target_page_id, episodeHandlerId=episode_handler_id)
        create_directive_output = CreateDirectiveOutput()
        create_directive_use_case.execute(create_directive_input, create_directive_output, self._fake_data)
        return create_directive_output.getDirectiveDTO()

    def _get_episode_handler_dto(self, episode_handler_id: str) -> EpisodeHandlerDTO:
        use_case = GetEpisodeHandlerUseCase()
        _input = GetEpisodeHandlerInput(episodeHandlerId=episode_handler_id)
        _output = GetEpisodeHandlerOutput()
        use_case.execute(_input, _output)
        return _output.getEpisodeHandlerDTO()

    def _get_input_example(self, app_element: AppElement):
        if app_element.getPlaceholder() != "":
            return InputExample(guid=0, text_a=app_element.getPlaceholder(), label=0)
        elif app_element.getLabel() != "":
            return InputExample(guid=0, text_a=app_element.getLabel(), label=0)
        elif app_element.getName() != "":
            return InputExample(guid=0, text_a=app_element.getName(), label=0)
        else:
            return None

    def _execute_action(self, app_element: AppElement, target_url) -> ExecuteActionOutput:
        final_submit = False
        input_example = self._get_input_example(app_element)
        episode_handler_entity = self._episode_handler_repository.findById(self._episode_handler_id)
        episode_handler = EpisodeHandlerEntityMapper.mappingEpisodeHandlerForm(episode_handler_entity)
        states = episode_handler.getAllState()

        preds = None
        fake_preds = None

        if input_example is not None:
            data_loader = PromptModelDirector().get_prompt_data_loader(self.prompt_model_builder, input_example)
            fake_data_loader = PromptModelDirector().get_prompt_data_loader(self.fake_prompt_model_builder, input_example)

            for step, batch in enumerate(data_loader):
                if torch.cuda.is_available():
                    batch = batch.cuda()
                logits = self.prompt_model(batch)
                preds = torch.argmax(logits, dim=-1)
            for step, batch in enumerate(fake_data_loader):
                if torch.cuda.is_available():
                    batch = batch.cuda()
                logits = self.fake_prompt_model(batch)
                fake_preds = torch.argmax(logits, dim=-1)

        execute_action_use_case = ExecuteActionUseCase(self.__aut_operator)
        doc = etree.parse(StringIO(states[-1].getDOM()), etree.HTMLParser())
        # find the submit button by xpath
        app_element_by_xpath = doc.xpath(app_element.getXpath())[0]
        str1 = 'The Form element:\n' + etree.tostring(doc.xpath(self.__target_form_xpath)[0], pretty_print=True, method="html", encoding="unicode") + '\nThe target element:\n' + etree.tostring(app_element_by_xpath, pretty_print=True, method="html", encoding="unicode")
        is_submit_button = False

        system_prompt = SystemPromptFactory.get("is_submit_button")
        is_submit_button_str = self._llm_service.get_response(str1, system_prompt).lower()
        if is_submit_button_str == "yes":
            is_submit_button = True

        # if app_element.getTagName() == "button" or app_element.getTagName() == "a" or (app_element.getTagName() == 'input' and (app_element.getType() == 'submit' or app_element.getType() == "button" or app_element.getType() == 'image')):
        #     is_submit_button = True

        execute_action_output = ExecuteActionOutput()

        if is_submit_button:
            action_number = 0
            final_submit = True
        elif not is_submit_button and app_element.getTagName() == "button":
            action_number = -1
        elif preds is not None and fake_preds is not None:
            if self._check_is_password(app_element):
                action_number = 25
            else:
                action_number = preds + 1
        else:
            execute_action_output.setIsDone(True)
            return execute_action_output

        execute_action_input = ExecuteActionInput(action_number, self._episode_handler_id, self.__server_name, target_url,
                                                  app_element.getXpath())

        try:
            execute_action_use_case.execute(input=execute_action_input, output=execute_action_output)
            episode_handler_entity = self._episode_handler_repository.findById(self._episode_handler_id)
            episode_handler = EpisodeHandlerEntityMapper.mappingEpisodeHandlerForm(episode_handler_entity)
            state: State = episode_handler.getAllState()[-2]
            self._fake_data[state.getId()] = fake_preds
        except Exception as exception:
            self._logger.exception(f"Something wrong when execute action: {exception}")
            traceback.print_exc()
            execute_action_output.setIsDone(True)
        finally:
            if final_submit:
                execute_action_output.setIsDone(True)
        return execute_action_output

    def _is_legal_directive(self):
        episode_handler_entity = self._episode_handler_repository.findById(self._episode_handler_id)
        episode_handler = EpisodeHandlerEntityMapper.mappingEpisodeHandlerForm(episode_handler_entity)
        states = episode_handler.getAllState()
        # When the length of states is less than 2, it means that the current state is the first state
        # or the app element is none and then final submit and the is_legal directive is false in this case
        # episode_handler.remain_only_index_zero_state() will remove states so that the length of states is less than 2
        if len(states) < 2:
            return False
        if states[-2].getActionType() == "click" and states[-2].getInteractedElement():
            interactive_app_element: AppElement = states[-2].getInteractedElement()
            tag_name = interactive_app_element.getTagName()
            tag_type = interactive_app_element.getType()
            if tag_name == "button" or tag_name == "a" or (tag_name == 'input' and (
                    tag_type == 'submit' or tag_type == "button" or tag_type == 'image')):
                after_action_dom = states[-1].getDOM()
                before_action_dom = states[-2].getDOM()
                return self._directive_rule_service.isLegal(self._target_page_id, before_action_dom, after_action_dom)
        return False

    def _remove_target_page(self):
        remove_target_page_use_case = RemoveTargetPageUseCase()
        remove_target_page_input = RemoveTargetPageInput(self._target_page_id)
        remove_target_page_output = RemoveTargetPageOutput()
        remove_target_page_use_case.execute(remove_target_page_input, remove_target_page_output)
        return remove_target_page_output

    def _reset_environment(self) -> ResetEnvironmentOutput:
        reset_env_use_case = ResetEnvironmentUseCase(self.__aut_operator)
        reset_env_use_input = ResetEnvironmentInput(self._episodeIndex)
        reset_env_use_output = ResetEnvironmentOutput()
        try:
            reset_env_use_case.execute(reset_env_use_input, reset_env_use_output)
            return reset_env_use_output
        except NosuchElementException:
            raise NosuchElementException("NoSuchElementException when reset environment")
        except RuntimeError:
            self.__aut_controller.resetAUTServer(True)
            reset_env_use_case.execute(reset_env_use_input, reset_env_use_output)
