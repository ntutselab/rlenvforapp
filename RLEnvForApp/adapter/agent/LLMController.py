import json
import os
import re
import traceback
from urllib.parse import urlparse

import torch
from dependency_injector.wiring import inject, Provide
from openprompt import PromptDataLoader
from openprompt.data_utils import InputExample

from RLEnvForApp.adapter.environment.autOperator.codeCoverageCollector.IstanbulMiddlewareCodeCoverageCollector import \
    IstanbulMiddlewareCodeCoverageCollector
from RLEnvForApp.adapter.environment.autOperator.codeCoverageCollector.NoCodeCoverageCollector import \
    NoCodeCoverageCollector
from RLEnvForApp.adapter.targetPagePort.FileManager import FileManager
from RLEnvForApp.domain.environment.actionCommand.InitiateToTargetActionCommand import NosuchElementException
from RLEnvForApp.domain.targetPage.DirectiveRuleService.FormSubmitCriteriaSingleton import FormSubmitCriteriaSingleton
from RLEnvForApp.logger.logger import Logger
from RLEnvForApp.adapter.agent.model.builder.PromptModelBuilder import PromptModelBuilder
from RLEnvForApp.adapter.agent.model.builder.PromptModelDirector import PromptModelDirector
from RLEnvForApp.adapter.controller.ApplicationUnderTestController import ApplicationUnderTestController
from RLEnvForApp.adapter.environment.autOperator.crawler.SeleniumCrawler import SeleniumCrawler
from RLEnvForApp.adapter.targetPagePort.factory.TargetPagePortFactory import TargetPagePortFactory
from RLEnvForApp.domain.environment.state.AppElement import AppElement
from RLEnvForApp.domain.targetPage.DirectiveRuleService.IDirectiveRuleService import IDirectiveRuleService
from RLEnvForApp.usecase.environment.autOperator.AIGUIDEOperator import AIGUIDEOperator
from RLEnvForApp.usecase.environment.autOperator.codeCoverageCollector.ICodeCoverageCollector import \
    ICodeCoverageCollector
from RLEnvForApp.usecase.environment.episodeHandler.dto.EpisodeHandlerDTO import EpisodeHandlerDTO
from RLEnvForApp.usecase.environment.episodeHandler.get.GetEpisodeHandlerInput import GetEpisodeHandlerInput
from RLEnvForApp.usecase.environment.episodeHandler.get.GetEpisodeHandlerOutput import GetEpisodeHandlerOutput
from RLEnvForApp.usecase.environment.episodeHandler.get.GetEpisodeHandlerUseCase import GetEpisodeHandlerUseCase
from RLEnvForApp.usecase.environment.executeAction.ExecuteActionInput import ExecuteActionInput
from RLEnvForApp.usecase.environment.executeAction.ExecuteActionOutput import ExecuteActionOutput
from RLEnvForApp.usecase.environment.executeAction.ExecuteActionUseCase import ExecuteActionUseCase
from RLEnvForApp.usecase.environment.resetEnvironment.ResetEnvironmentUseCase import *
from RLEnvForApp.usecase.environment.state.dto.stateDTO import StateDTO
from RLEnvForApp.usecase.repository.TargetPageRepository import TargetPageRepository
from RLEnvForApp.usecase.targetPage.create.CreateDirectiveInput import CreateDirectiveInput
from RLEnvForApp.usecase.targetPage.create.CreateDirectiveOutput import CreateDirectiveOutput
from RLEnvForApp.usecase.targetPage.create.CreateDirectiveUseCase import CreateDirectiveUseCase
from RLEnvForApp.usecase.targetPage.dto.DirectiveDTO import DirectiveDTO
from RLEnvForApp.usecase.targetPage.dto.TargetPageDTO import TargetPageDTO
from RLEnvForApp.usecase.targetPage.get.GetTargetPageInput import GetTargetPageInput
from RLEnvForApp.usecase.targetPage.get.GetTargetPageOutput import GetTargetPageOutput
from RLEnvForApp.usecase.targetPage.get.GetTargetPageUseCase import GetTargetPageUseCase
from RLEnvForApp.usecase.targetPage.remove.RemoveTargetPageInput import RemoveTargetPageInput
from RLEnvForApp.usecase.targetPage.remove.RemoveTargetPageOutput import RemoveTargetPageOutput
from RLEnvForApp.usecase.targetPage.remove.RemoveTargetPageUseCase import RemoveTargetPageUseCase


class LLMController:

    @inject
    def __init__(self,
                 episode_handler_repository: EpisodeHandlerRepository =
                    Provide[EnvironmentDIContainers.episodeHandlerRepository],
                 directive_rule_service: IDirectiveRuleService =
                    Provide[EnvironmentDIContainers.directiveRuleService],
                 repository: TargetPageRepository = Provide[EnvironmentDIContainers.targetPageRepository]):
        self._formCounts = {}
        self._directive_rule_service = directive_rule_service
        self._episode_handler_repository = episode_handler_repository
        self._repository = repository
        self.__server_name = "keystonejs_with_coverage"
        self.__application_ip = "127.0.0.1"
        self.__application_port = 3100
        self.__code_coverage_type = "statement coverage"
        self._logger = Logger()
        self._logger.info("Init LLM.Env")
        self.__aut_controller = ApplicationUnderTestController(applicationName=self.__server_name,
                                                               serverIP=self.__application_ip,
                                                               port=self.__application_port)
        self.__crawler = SeleniumCrawler("Chrome")
        self.__code_coverage_collector: ICodeCoverageCollector = IstanbulMiddlewareCodeCoverageCollector(
                serverIp=self.__application_ip, serverPort=self.__application_port)
        self.__aut_operator = AIGUIDEOperator(
            crawler=self.__crawler, codeCoverageCollector=self.__code_coverage_collector)
        self.__target_page_port = TargetPagePortFactory().createAIGuideTargetPagePort(javaIp="127.0.0.1",
                                                                                      pythonIp="127.0.0.1",
                                                                                      javaPort=2700, pythonPort=2701,
                                                                                      serverName=self.__server_name,
                                                                                      rootUrl=f"http://{self.__application_ip}:{self.__application_port}/",
                                                                                      codeCoverageType=self.__code_coverage_type)
        self.__target_page_port.connect()

        self.__target_form_xpath = ''
        self.__form_counts = {}
        self._target_page_id = ""
        self._episodeIndex = 0

        if torch.cuda.is_available():
            self._logger.info("CUDA is available")
            torch.cuda.empty_cache()

        self.__aut_controller.startAUTServer()

        self.prompt_model_builder = PromptModelBuilder()
        self.prompt_model = PromptModelDirector().make_my_research(self.prompt_model_builder)
        # check cuda
        if torch.cuda.is_available():
            self.prompt_model = self.prompt_model.cuda()

    def play(self):
        while True:
            if len(self._repository.findAll()) == 0:
                self.__target_page_port.waitForTargetPage()
            is_legal_directive = False
            self.__aut_controller.resetAUTServer(True)
            self._episodeIndex += 1
            reset_env_use_case = ResetEnvironmentUseCase(operator=self.__aut_operator)
            reset_env_use_input = ResetEnvironmentInput.ResetEnvironmentInput(
                episodeIndex=self._episodeIndex)
            reset_env_use_output = ResetEnvironmentOutput.ResetEnvironmentOutput()
            try:
                reset_env_use_case.execute(input=reset_env_use_input, output=reset_env_use_output)
            except NosuchElementException:
                continue
            except RuntimeError:
                self.__aut_controller.resetAUTServer(True)
                reset_env_use_case.execute(input=reset_env_use_input, output=reset_env_use_output)

            FormSubmitCriteriaSingleton.getInstance().setFormSubmitCriteria(applicationName=self.__server_name,
                                                                            url=reset_env_use_output.getTargetPageUrl(), xpath=reset_env_use_output.getFormXPath())
            self._episodeHandlerId = reset_env_use_output.getEpisodeHandlerId()
            self._target_page_id = reset_env_use_output.getTargetPageId()
            self._episodeHandlerId = reset_env_use_output.getEpisodeHandlerId()

            while not is_legal_directive:
                app_element: AppElement = self.__aut_operator.getFocusedAppElement()
                if app_element is None:
                    if len(self.__aut_operator.getAllSelectedAppElements()) == 0:
                        remove_target_page_use_case = RemoveTargetPageUseCase()
                        remove_target_page_input = RemoveTargetPageInput(targetPageId=self._target_page_id)
                        remove_target_page_output = RemoveTargetPageOutput()
                        remove_target_page_use_case.execute(input=remove_target_page_input, output=remove_target_page_output)
                    break
                input_example = None
                result_label = None

                # Check the input element what it is type
                if app_element.getPlaceholder() != "":
                    input_example = InputExample(guid=0, text_a=app_element.getPlaceholder(), label=0)
                elif app_element.getLabel() != "":
                    input_example = InputExample(guid=0, text_a=app_element.getLabel(), label=0)
                elif app_element.getName() != "":
                    input_example = InputExample(guid=0, text_a=app_element.getName(), label=0)

                if input_example is not None:
                    data_loader = PromptDataLoader(
                        dataset=[input_example],
                        tokenizer=self.prompt_model_builder.tokenizer,
                        template=self.prompt_model_builder.template,
                        tokenizer_wrapper_class=self.prompt_model_builder.wrapper_class,
                        max_seq_length=480,
                        decoder_max_length=3,
                        batch_size=1, shuffle=False,
                        teacher_forcing=False,
                        predict_eos_token=False,
                        truncate_method="tail"
                    )

                    preds = None
                    for step, batch in enumerate(data_loader):
                        if torch.cuda.is_available():
                            batch = batch.cuda()
                        logits = self.prompt_model(batch)
                        preds = torch.argmax(logits, dim=-1)

                final_submit = False
                execute_action_use_case = ExecuteActionUseCase(
                    autOperator=self.__aut_operator)
                if app_element.getTagName() == "button" or app_element.getTagName() == "a" or (app_element.getTagName() == 'input' and (
                        app_element.getType() == 'submit' or app_element.getType() == "button" or app_element.getType() == 'image')):
                    execute_action_input = ExecuteActionInput(
                        actionNumber=0, episodeHandlerId=self._episodeHandlerId, aut_name=self.__server_name, url=reset_env_use_output.getTargetPageUrl(), xpath=app_element.getXpath())
                    final_submit = True
                else:
                    if self.check_is_password(app_element):
                        execute_action_input = ExecuteActionInput(
                            actionNumber=25, episodeHandlerId=self._episodeHandlerId, aut_name=self.__server_name, url=reset_env_use_output.getTargetPageUrl(), xpath=app_element.getXpath())
                    else:
                        execute_action_input = ExecuteActionInput(
                            actionNumber=int(preds + 1), episodeHandlerId=self._episodeHandlerId, aut_name=self.__server_name, url=reset_env_use_output.getTargetPageUrl(), xpath=app_element.getXpath())
                execute_action_output = ExecuteActionOutput()

                try:
                    execute_action_use_case.execute(input=execute_action_input, output=execute_action_output)
                except Exception as exception:
                    self._logger.exception(f"Something wrong when execute action: {exception}")
                    traceback.print_exc()
                    execute_action_output.setIsDone(True)

                if self._target_page_id not in self._formCounts:
                    self._formCounts[self._target_page_id] = 1

                if final_submit:
                    episode_handler_entity = self._episode_handler_repository.findById(
                        id=self._episodeHandlerId)
                    episode_handler = EpisodeHandlerEntityMapper.mappingEpisodeHandlerForm(
                        episode_handler_entity)
                    states = episode_handler.getAllState()
                    if states[-2].getActionType() == "click" and states[-2].getInteractedElement():
                        interactive_app_element: AppElement = states[-2].getInteractedElement()
                        tag_name = interactive_app_element.getTagName()
                        tag_type = interactive_app_element.getType()
                        if tag_name == "button" or tag_name == "a" or (tag_name == 'input' and (
                                tag_type == 'submit' or tag_type == "button" or tag_type == 'image')):
                            after_action_dom = states[-1].getDOM()
                            before_action_dom = states[-2].getDOM()
                            is_legal_directive = self._directive_rule_service.isLegal(
                                targetPageId=self._target_page_id, beforeActionDom=before_action_dom,
                                afterActionDom=after_action_dom)

                if final_submit and is_legal_directive:
                    try:
                        self._logger.info(f"Find legal directive, target page id: {self._target_page_id}")
                        self._logger.info(f"Number of attempts: {self._formCounts[self._target_page_id]}")
                        self.__target_page_port.pushTargetPage(targetPageId=self._target_page_id,
                                                               episodeHandlerId=self._episodeHandlerId)
                    except Exception as ex:
                        template = 'An exception of type {0} occurred. Arguments:\n{1!r}'
                        message = template.format(type(ex).__name__, ex.args)
                        self._logger.info(message)
                        self._logger.info(f"PUSH ERROR!!! {self.__crawler.getUrl()}")
                elif final_submit and not is_legal_directive:
                    # TODO: This is a temporary solution by AI, need to be checked by human
                    self._formCounts[self._target_page_id] += 1
                    self._logger.info(f"Find illegal directive, target page id: {self._target_page_id}")
                    self._logger.info(f"Number of attempts: {self._formCounts[self._target_page_id]}")
                    if self._formCounts[self._target_page_id] >= 10:
                        self._formCounts[self._target_page_id] = 0
                        directive_dto = self._createDirective(targetPageId=self._target_page_id, episodeHandlerId=self._episodeHandlerId)
                        self._saveTargetPageToHtmlSet(episodeHandlerId=self._episodeHandlerId,directiveDTO=directive_dto)
                        remove_target_page_use_case = RemoveTargetPageUseCase()
                        remove_target_page_input = RemoveTargetPageInput(targetPageId=self._target_page_id)
                        remove_target_page_output = RemoveTargetPageOutput()
                        remove_target_page_use_case.execute(input=remove_target_page_input, output=remove_target_page_output)
                        break

    def check_is_password(self, app_element: AppElement):
        # check if the element is a password field use regex
        if re.match(r'password', app_element.getName(), re.IGNORECASE) or re.match(r'password', app_element.getLabel(), re.IGNORECASE) or re.match(r'password', app_element.getPlaceholder(), re.IGNORECASE):
            return True
        return False

    def _saveTargetPageToHtmlSet(self, episodeHandlerId: str, directiveDTO: DirectiveDTO):
        file_name = f"{self.__server_name}_{urlparse(directiveDTO.getUrl()).path.replace('/', '_')}_{directiveDTO.getFormXPath().replace('/', '_')}"
        initial_state_dto: StateDTO = self._getEpisodeHandlerDTO(
            episodeHandlerId=episodeHandlerId).getStateDTOs()[0]

        interactive_app_element_dictionary = []
        directive_dictionary = {}
        for app_event_dto in directiveDTO.getAppEventDTOs():
            directive_dictionary[app_event_dto.getXpath()] = {
                "value": app_event_dto.getValue(), "category": app_event_dto.getCategory()}
        for app_element_dto in initial_state_dto.getSelectedAppElementDTOs():
            interactive_app_element_dictionary.append(app_element_dto.getXpath())
        form_x_path = directiveDTO.getFormXPath()
        directive_log_json = json.dumps({"interactive_appElement": interactive_app_element_dictionary,
                                       "appEvent": directive_dictionary, "formXPath": form_x_path})

        # self._updateInputValueWeights(directiveDictionary)

        Logger().info(f"Save html set:\n{file_name}\n{form_x_path}\n{directive_dictionary}")

        file_manager = FileManager()
        file_manager.createFolder("htmlSet", "FAILED_HTML_SET")
        file_manager.createFile(path=os.path.join("htmlSet", "FAILED_HTML_SET"),
                               fileName=file_name + ".html", context=directiveDTO.getDom())
        file_manager.createFile(path=os.path.join("htmlSet", "FAILED_HTML_SET"),
                               fileName=file_name + ".json", context=directive_log_json)

    def _createDirective(self, targetPageId: str, episodeHandlerId: str):
        create_directive_use_case = CreateDirectiveUseCase()
        create_directive_input = CreateDirectiveInput(
            targetPageId=targetPageId, episodeHandlerId=episodeHandlerId)
        create_directive_output = CreateDirectiveOutput()
        create_directive_use_case.execute(create_directive_input, create_directive_output)

        return create_directive_output.getDirectiveDTO()

    def _getEpisodeHandlerDTO(self, episodeHandlerId: str) -> EpisodeHandlerDTO:
        usecase = GetEpisodeHandlerUseCase()
        input = GetEpisodeHandlerInput(episodeHandlerId=episodeHandlerId)
        output = GetEpisodeHandlerOutput()

        usecase.execute(input=input, output=output)
        return output.getEpisodeHandlerDTO()