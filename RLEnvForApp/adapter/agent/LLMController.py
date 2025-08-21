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
from RLEnvForApp.domain.targetPage.FeedbackRuleService.FormFieldFeedbackRuleService import FormFieldFeedbackRuleService
from RLEnvForApp.domain.targetPage.FeedbackRuleService.IFeedbackRuleService import IFeedbackRuleService
from RLEnvForApp.domain.targetPage.FieldRuleService.IFieldRuleService import IFieldRuleService
from RLEnvForApp.domain.formInput.textGeneration.ITextGenerationService import ITextGenerationService
from RLEnvForApp.domain.constants.actions import ACTION_NUMBER
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
from RLEnvForApp.usecase.formElement.FormElementUseCase import FormElementUseCase
from RLEnvForApp.usecase.formElement.FormElementOutput import FormElementOutput
from RLEnvForApp.usecase.formElement.FormElementInput import FormElementInput
from RLEnvForApp.application.timer.ExecutionTimer import ExecutionTimer
from configuration.di.EnvironmentDIContainers import EnvironmentDIContainers


class LLMController:

    @inject
    def __init__(self,
                 episode_handler_repository: EpisodeHandlerRepository =
                 Provide[EnvironmentDIContainers.episodeHandlerRepository],
                 directive_rule_service: IDirectiveRuleService =
                 Provide[EnvironmentDIContainers.directiveRuleService],
                 field_rule_service: IFieldRuleService =
                 Provide[EnvironmentDIContainers.fieldRuleService],
                 feedbacl_rule_service: IFeedbackRuleService = 
                 Provide[EnvironmentDIContainers.feedbackRuleService],
                 repository: TargetPageRepository = Provide[EnvironmentDIContainers.targetPageRepository],
                 text_generation_service: ITextGenerationService = Provide[EnvironmentDIContainers.textGenerationService],
                 llm_service : ILlmService = Provide[EnvironmentDIContainers.llmService],
                 ):
        self._llm_service = llm_service
        LlmServiceContainer.llm_service_instance.set_instance(llm_service)

        ExecutionTimer.init_instance()
        self.__timer = ExecutionTimer.get_instance()

        self._fake_data = {}
        self._episode_handler_id = None
        self._form_counts = {}
        self._form_retry_count = {}
        self._directive_rule_service = directive_rule_service
        self._episode_handler_repository = episode_handler_repository
        self._repository = repository
        # self.__server_name = "timeoff_management_with_coverage"
        # self.__server_name = "astuto"
        # self.__server_name = "nodebb_with_coverage"
        # self.__server_name = "keystonejs_with_coverage"
        # self.__server_name = "django_blog_with_no_coverage"
        # self.__server_name = "spring_petclinic_with_no_coverage"
        self.__server_name = "timeoff_management_with_coverage"
        # self.__server_name = "oscar"
        # self.__server_name = "kimai"
        
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
        self._target_page_id = ""
        self._episodeIndex = 0
        self.__aut_controller.startAUTServer()

        self.prompt_model_builder = PromptModelBuilder()
        self.fake_prompt_model_builder = PromptModelBuilder()
        self.pre_fields = []
        self.__form_feedbacks = {}
        # TODO: make _form_feedback_rule_service and _field_rule_service provide by Configuration
        self._form_feedback_rule_service = feedbacl_rule_service
        self._field_rule_service = field_rule_service
        self._form_element_usecase = FormElementUseCase(llm_service=self._llm_service, field_rule_service = self._field_rule_service)
        self._reset_env_use_case = None

        self._text_generation_service = text_generation_service

        # record feedback per trying filling form
        self._feedbacks_records = {} 
        self._every_form_time_summary = {}
        # self.prompt_model = PromptModelDirector().make_my_research(self.prompt_model_builder)
        # self.fake_prompt_model = PromptModelDirector().make_fake_prompt_model(self.fake_prompt_model_builder)
        # # check cuda
        # if torch.cuda.is_available():
        #     self._logger.info("CUDA is available")
        #     torch.cuda.empty_cache()
        #     self.prompt_model = self.prompt_model.cuda()
        #     self.fake_prompt_model = self.fake_prompt_model.cuda()

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

            # FormSubmitCriteriaSingleton.getInstance().setFormSubmitCriteria(applicationName=self.__server_name,
            #                                                                 url=reset_env_use_output.getTargetPageUrl(),
            #                                                                 xpath=reset_env_use_output.getFormXPath())
            self._target_page_id = reset_env_use_output.getTargetPageId()
            self._episode_handler_id = reset_env_use_output.getEpisodeHandlerId()
            self.__target_form_xpath = reset_env_use_output.getFormXPath()
            self._start_timer()
            self._feedbacks_records = {} 
            while not is_legal_directive:
                try_count = self._form_retry_count.get(self._target_page_id)
                
                if try_count is None:
                    try_count = 0
                app_element: AppElement = self.__aut_operator.getFocusedAppElement()
                if app_element is None:
                    self._logger.info("App element is None")
                    if len(self.__aut_operator.getAllSelectedAppElements()) == 0:
                        self._logger.info("No app element")
                        self._remove_target_page()
                    break
                final_submit = self._execute_action(app_element, reset_env_use_output.getTargetPageUrl())

                if self._target_page_id not in self._form_retry_count:
                    self._form_retry_count[self._target_page_id] = 1

                if final_submit.getIsDone():
                    is_legal_directive = self._is_legal_directive()

                if final_submit.getIsDone() and is_legal_directive:
                    try:
                        self._logger.info(f"Find legal directive, target page id: {self._target_page_id}")
                        self._logger.info(f"Number of attempts: {self._form_retry_count[self._target_page_id]}")
                        # directive_dto = self._create_fake_directive(self._target_page_id, self._episode_handler_id)
                        # self.__target_page_port.push_target_page_by_directive(self._target_page_id, directive_dto)
                        self.__target_page_port.pushTargetPage(self._target_page_id, self._episode_handler_id)
                        self._record_form_time(self.__target_form_xpath, reset_env_use_output.getTargetPageUrl(), self._form_retry_count[self._target_page_id])
                        self._save_execution_time_summary(reset_env_use_output.getTargetPageUrl())
                        self._save_feedback_and_try_count(reset_env_use_output.getTargetPageUrl())
                        self._fake_data = {}
                        self.pre_fields = []
                        # self._stop_timer()
                        
                    except Exception as ex:
                        self._logger.info(f"Error when push target page: {ex}")
                        template = 'An exception of type {0} occurred. Arguments:\n{1!r}'
                        message = template.format(type(ex).__name__, ex.args)
                        self._logger.info(message)
                        self._fake_data = {}
                        self._logger.info(f"PUSH ERROR!!! {self.__crawler.getUrl()}")
                elif final_submit.getIsDone() and not is_legal_directive:
                    # TODO: This is a temporary solution by AI, need to be checked by human
                    feedback = self._get_feedback()
                    self.__form_feedbacks[self._target_page_id] = feedback
                    self._logger.info(f"Feedback: {self.__form_feedbacks[self._target_page_id]}")
                    self._feedbacks_records[self._form_retry_count[self._target_page_id]] = feedback
                    self._record_form_time(self.__target_form_xpath, reset_env_use_output.getTargetPageUrl(), self._form_retry_count[self._target_page_id])
                    
                    if self._form_retry_count[self._target_page_id] < 10:
                        self._retry_filling_form()
                        self._logger.info(f"url: {reset_env_use_output.getTargetPageUrl()}")
                        self._start_timer()
                    else:
                        directive_dto = self._create_directive(self._target_page_id, self._episode_handler_id)
                        self._save_target_page_to_html_set(self._episode_handler_id, directive_dto)
                        self._save_execution_time_summary(reset_env_use_output.getTargetPageUrl())
                        self._save_feedback_and_try_count(reset_env_use_output.getTargetPageUrl())
                        self._form_retry_count[self._target_page_id] = 0
                        self._remove_target_page()
                        # self._stop_timer()
                        break
                    self._logger.info(f"Try again, target page id: {self._target_page_id}")
                    

    def _check_is_password(self, app_element: AppElement):
        # check if the element is a password field use regex
        if app_element.getType() == "password" or re.search(r'password', app_element.getName(), re.IGNORECASE) or re.search(r'password', app_element.getLabel(),
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

        self._logger.info(f"Save html set:\n{file_name}\n{form_x_path}\n{directive_dictionary}")

        file_manager = FileManager()
        file_manager.createFolder("htmlSet", "FAILED_HTML_SET")
        file_manager.createFile(path=os.path.join("htmlSet", "FAILED_HTML_SET"),
                                fileName=file_name + ".html", context=directive_dto.getDom())
        file_manager.createFile(path=os.path.join("htmlSet", "FAILED_HTML_SET"),
                                fileName=file_name + ".json", context=directive_log_json)

    def _save_execution_time_summary(self, url):
        url = url
        form_xpath =  self.__target_form_xpath
        file_name = f"{self.__server_name}_executionSummary"
        time_summary_json = json.dumps(self._every_form_time_summary)

        file_manager = FileManager()
        file_manager.createFolder(".", "executionSummary")
        file_manager.createFile(
            path="executionSummary",
            fileName=file_name + ".json",
            context=time_summary_json
        )

    def _save_feedback_and_try_count(self, url):
        # TODO: Find better way to get the url like hemlset
        url = url
        form_xpath =  self.__target_form_xpath
        file_name = f"{self.__server_name}_{urlparse(url).path.replace('/', '_')}_{form_xpath.replace('/', '_')}"
        feedback_and_try_count_json = json.dumps(self._feedbacks_records)

        self._logger.info(f"save file_name: {file_name}")
        self._logger.info(f"content: {feedback_and_try_count_json}")
        file_manager = FileManager()
        file_manager.createFolder(".", "feedbackRecord")
        file_manager.createFile(
            path="feedbackRecord",
            fileName=file_name + ".json",
            context=feedback_and_try_count_json
        )

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
    def _handle_form_element(self, target_page_dom:str, target_form_xpath:str, target_element_xpath:str, app_element: AppElement, target_url: str) -> FormElementOutput:
        
        feedback = self.__form_feedbacks.get(self._target_page_id)
        if feedback is None:
            feedback = {}
        try_count = self._form_retry_count.get(self._target_page_id)
        if try_count is None:
            try_count = 0
        form_title = self._getFormTitle(target_page_dom, self.__target_form_xpath)
        pre_fields = self.pre_fields

        form_element_input = FormElementInput(
            target_page_dom=target_page_dom,
            target_form_xpath=target_form_xpath,
            target_element_xpath=target_element_xpath,
            feedback=feedback,
            try_count=try_count,
            app_element=app_element,
            form_title=form_title,
            pre_fields=pre_fields
        )
        return self._form_element_usecase.handle(formElementInput=form_element_input)
    
    def _execute_action(self, app_element: AppElement, target_url) -> ExecuteActionOutput:
        # TODE: Find form title
        self._logger.info(f"tag:{app_element.getTagName()},Type:{app_element.getType()} ,  Execute action name: {app_element.getName()}, label: {app_element.getLabel()}, xpath: {app_element.getXpath()}")
        final_submit = False
        episode_handler_entity = self._episode_handler_repository.findById(self._episode_handler_id)
        episode_handler = EpisodeHandlerEntityMapper.mappingEpisodeHandlerForm(episode_handler_entity)
        states = episode_handler.getAllState()
        execute_action_use_case = ExecuteActionUseCase(self.__aut_operator)
        self._logger.info(f"doc: {etree.parse(StringIO(states[-1].getDOM()), etree.HTMLParser())}")
        target_page_dom = states[-1].getDOM()
        
       
        # doc_tree = etree.parse(StringIO(states[-1].getDOM()), etree.HTMLParser())
        # doc = doc_tree.getroot() 
        doc = etree.parse(StringIO(states[-1].getDOM()), etree.HTMLParser())
        execute_action_output = ExecuteActionOutput()
        app_element_by_xpath = None
        target_form_xpath = None
        target_element_xpath = None
        try:
            app_element_by_xpath = doc.xpath(app_element.getXpath())[0]
            target_form_xpath = etree.tostring(doc.xpath(self.__target_form_xpath)[0], pretty_print=True, method="html", encoding="unicode")
            target_element_xpath = etree.tostring(app_element_by_xpath, pretty_print=True, method="html", encoding="unicode")
        except Exception as e:
            print(f"[XPath error] {e}")
            return execute_action_output

        action_number = 0
        execute_action_output = ExecuteActionOutput()
        form_element_output = self._handle_form_element(target_page_dom, target_form_xpath, target_element_xpath, app_element, target_url)
        final_submit = form_element_output.get_final_submit()
        action_number = form_element_output.get_action_number()
        prompt = form_element_output.get_prompt()
        self._logger.info(f"Pre fields: {self.pre_fields}")
        try_count = self._form_retry_count.get(self._target_page_id)  
        if try_count is None:
            try_count = 0
        feedback = self.__form_feedbacks.get(self._target_page_id)
        if feedback is None:
            feedback = {}
        is_element_in_feedback = False
        if app_element.getXpath() in feedback:
            is_element_in_feedback = True

        execute_action_input = ExecuteActionInput(action_number, self._episode_handler_id, self.__server_name, target_url,
                                                  app_element.getXpath(), prompt, try_count, is_element_in_feedback, self._text_generation_service,)

        try:
            execute_action_use_case.execute(input=execute_action_input, output=execute_action_output)
            episode_handler_entity = self._episode_handler_repository.findById(self._episode_handler_id)
            episode_handler = EpisodeHandlerEntityMapper.mappingEpisodeHandlerForm(episode_handler_entity)
            state: State = episode_handler.getAllState()[-2]
            if action_number == ACTION_NUMBER["input"] or action_number == ACTION_NUMBER["select"] or action_number == ACTION_NUMBER["checkbox"]:
                pre_field = {"name": app_element.getName(), "label": app_element.getLabel(), "placeholder": app_element.getPlaceholder(), "value": state.getAppEventInputValue(), "xpath": app_element.getXpath()}
                
                self.pre_fields.append(pre_field)
            # self._fake_data[state.getId()] = preds
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

    def _get_feedback(self):
        episode_handler_entity = self._episode_handler_repository.findById(self._episode_handler_id)
        episode_handler = EpisodeHandlerEntityMapper.mappingEpisodeHandlerForm(episode_handler_entity)
        states = episode_handler.getAllState()
        # When the length of states is less than 2, it means that the current state is the first state
        # or the app element is none and then final submit and the is_legal directive is false in this case
        # episode_handler.remain_only_index_zero_state() will remove states so that the length of states is less than 2
        if len(states) < 2:
            return {}
        if states[-2].getActionType() == "click" and states[-2].getInteractedElement():
            interactive_app_element: AppElement = states[-2].getInteractedElement()
            tag_name = interactive_app_element.getTagName()
            tag_type = interactive_app_element.getType()
            if tag_name == "button" or tag_name == "a" or (tag_name == 'input' and (
                    tag_type == 'submit' or tag_type == "button" or tag_type == 'image')):
                after_action_dom = states[-1].getDOM()
                before_action_dom = states[-2].getDOM()
                previous_feedbacks = self.__form_feedbacks.get(self._target_page_id, None)
                return self._form_feedback_rule_service.getFeedbackAndLocation(before_action_dom, after_action_dom, self.pre_fields, previous_feedbacks)
        return {}
    def _remove_target_page(self):
        remove_target_page_use_case = RemoveTargetPageUseCase()
        remove_target_page_input = RemoveTargetPageInput(self._target_page_id)
        remove_target_page_output = RemoveTargetPageOutput()
        remove_target_page_use_case.execute(remove_target_page_input, remove_target_page_output)
        return remove_target_page_output

    def _reset_environment(self) -> ResetEnvironmentOutput:
        self._reset_env_use_case = ResetEnvironmentUseCase(self.__aut_operator)
        reset_env_use_input = ResetEnvironmentInput(self._episodeIndex)
        reset_env_use_output = ResetEnvironmentOutput()
        try:
            self._reset_env_use_case.execute(reset_env_use_input, reset_env_use_output)
            return reset_env_use_output
        except NosuchElementException:
            raise NosuchElementException("NoSuchElementException when reset environment")
        except RuntimeError:
            self.__aut_controller.resetAUTServer(True)
            self._reset_env_use_case.execute(reset_env_use_input, reset_env_use_output)

    def _is_required(self, dom_str: str, xpath: str) -> bool:
        """
        檢查指定 XPath 的元素是否為必填。
        
        :param dom_str: HTML DOM 的字串表示
        :param xpath: 要檢查的 XPath
        :return: 如果該元素為必填則回傳 True，否則回傳 False
        """
        feedback = self.__form_feedbacks.get(self._target_page_id)
        self._logger.info(f"Start check required field: {xpath}")
        return self._field_rule_service.isLegal(dom_str=dom_str, xpath=xpath, feedback=feedback)
    
    def _retry_filling_form(self):
        self._logger.info(f"Find illegal directive, target page id: {self._target_page_id}")
        self._logger.info(f"Number of attempts: {self._form_retry_count[self._target_page_id]}")
        # 增加表單重試次數
        self._form_retry_count[self._target_page_id] += 1
        self._logger.info(f"Retry filling form updated try count: {self._form_retry_count[self._target_page_id]}")
        # 清除 fake data（準備下次重新填入）
        self._fake_data = {}
        
        # restart container
        self.__aut_controller.resetAUTServer(True)
        
        self._reset_env_use_case.retry_with_initial_config(self._episode_handler_id)
        episode_handler_entity = self._episode_handler_repository.findById(self._episode_handler_id)
        episode_handler = EpisodeHandlerEntityMapper.mappingEpisodeHandlerForm(episode_handler_entity)
        print(f"episode_handler.getAllState() length: {len(episode_handler.getAllState())}")
        
        self.pre_fields = []

    # TODO: Extract this to another class
    def _getFormTitle(self, dom, formXPath):
        # Get the form element from the DOM using XPath
        tree = etree.parse(StringIO(dom), etree.HTMLParser())
        form_elements = tree.xpath(formXPath)
        if not form_elements:
            return None
        form_el = form_elements[0]

        # 優先 legend
        legend = form_el.xpath('.//legend')
        if legend and legend[0].text:
            return legend[0].text.strip()

        # 再找前一個標題
        heading = form_el.xpath('preceding-sibling::*[self::h1 or self::h2 or self::h3 or self::p][1]')
        if heading and heading[0].text:
            return heading[0].text.strip()

        return None
    
    def _start_timer(self):
        self._logger.info("Start timer")
        self.__timer.start()
    
    def _stop_timer(self):
        duration = self.__timer.stop_and_accumulate()
        self._logger.info(f"Time Summary: {self.__timer.get_summary()}")
        self._save_execution_time_summary()
        return duration
    
    def _record_form_time(self, form_xpath, url, try_count):
        key = f"{self.__server_name}_{urlparse(url).path.replace('/', '_')}_{form_xpath.replace('/', '_')}"
        duration = self.__timer.stop_and_accumulate()
        
        print(f"[Form time] key is {key}, try count is {try_count}")
        print(self._every_form_time_summary)
        # 如果這個 form_xpath 還沒建立，初始化一個 dict
        if key not in self._every_form_time_summary:
            self._every_form_time_summary[key] = {}

        # 這次的 try_count 記錄
        self._every_form_time_summary[key][str(try_count)] = duration

        # 更新 total
        previous_total = self._every_form_time_summary[key].get("total", 0)
        new_total = previous_total + duration
        self._every_form_time_summary[key]["total"] = new_total

        self._logger.info(f"[Form Time] {key} Try #{try_count}: +{duration:.2f}s (Total so far: {new_total:.2f}s)")

        # update total time of form agent
         # 更新 total
        if "total" not in self._every_form_time_summary:
            self._every_form_time_summary["total"] = {}
        the_count_up_to_now = len(self._every_form_time_summary) - 1 
        form_agent_total = self._every_form_time_summary["total"].get(str(the_count_up_to_now-2),0) + new_total
        self._every_form_time_summary["total"][the_count_up_to_now] = form_agent_total

        self._logger.info(f"[Form Time] Form agent has execute so far: {form_agent_total:.2f}s)")
