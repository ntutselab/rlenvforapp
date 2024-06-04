from dependency_injector.wiring import Provide, inject

from RLEnvForApp.domain.environment.actionCommandFactoryService.LLMActionCommandFactory import LLMActionCommandFactory
from configuration.di.EnvironmentDIContainers import EnvironmentDIContainers
from RLEnvForApp.adapter.targetPagePort.FileManager import FileManager
# from RLEnvForApp.domain.environment.inputSpace import inputTypes
from RLEnvForApp.adapter.agent.model.builder.PromptModelDirector import PromptModelDirector
from RLEnvForApp.domain.environment.state.AppElement import AppElement
from RLEnvForApp.domain.environment.state.CodeCoverage import CodeCoverage
from RLEnvForApp.domain.environment.state.State import State
from RLEnvForApp.domain.targetPage.AppEvent import AppEvent
from RLEnvForApp.domain.targetPage.Directive import Directive
from RLEnvForApp.domain.targetPage.DirectiveRuleService.IDirectiveRuleService import \
    IDirectiveRuleService
from RLEnvForApp.usecase.environment.episodeHandler.mapper import EpisodeHandlerEntityMapper
from RLEnvForApp.usecase.repository.EpisodeHandlerRepository import EpisodeHandlerRepository
from RLEnvForApp.usecase.repository.TargetPageRepository import TargetPageRepository
from RLEnvForApp.usecase.targetPage.create import CreateDirectiveInput, CreateDirectiveOutput
from RLEnvForApp.usecase.targetPage.mapper import DirectiveDTOMapper, TargetPageEntityMapper


class CreateFakeDirectiveUseCase:
    @inject
    def __init__(self,
                 target_page_repository: TargetPageRepository = Provide[EnvironmentDIContainers.targetPageRepository],
                 episode_handler_repository: EpisodeHandlerRepository = Provide[
                     EnvironmentDIContainers.episodeHandlerRepository],
                 directive_rule_service: IDirectiveRuleService = Provide[EnvironmentDIContainers.directiveRuleService]):
        self._directiveRuleService: IDirectiveRuleService = directive_rule_service
        self._target_page_repository = target_page_repository
        self._episode_handler_repository = episode_handler_repository
        self.__input_type = PromptModelDirector.classes

    def execute(self, input: CreateDirectiveInput.CreateDirectiveInput,
                output: CreateDirectiveOutput.CreateDirectiveOutput,
                fake_data: {}):
        target_page_entity = self._target_page_repository.findById(input.getTargetPageId())
        target_page = TargetPageEntityMapper.mappingTargetPageFrom(target_page_entity)
        target_episode_handler_entity = self._episode_handler_repository.findById(input.getEpisodeHandlerId())
        episode_episode_handler = EpisodeHandlerEntityMapper.mappingEpisodeHandlerForm(target_episode_handler_entity)
        code_coverages: [CodeCoverage] = None
        app_events: [AppEvent] = []

        for state in episode_episode_handler.getAllState():
            action_type = state.getActionType()
            interactive_app_element: AppElement = state.getInteractedElement()
            code_coverages = state.getCodeCoverages()

            if interactive_app_element is None:
                continue

            if action_type == "changeFocus":
                continue
            if action_type == "click":
                if not interactive_app_element.getTagName() == "button" and not (
                        interactive_app_element.getTagName() == "input" and (
                        interactive_app_element.getType() == "submit" or interactive_app_element.getType() == "button" or interactive_app_element.getType() == "image" or interactive_app_element.getType() == "checkbox")):
                    continue
                app_events.append(AppEvent(xpath=interactive_app_element.getXpath(),
                                           value="", category="click"))
            if action_type == "input":
                if not interactive_app_element.getTagName() == "input" and not interactive_app_element.getTagName() == "textarea":
                    continue
                if fake_data.get(state.getId()) is None:
                    continue
                value = LLMActionCommandFactory._get_input_value(LLMActionCommandFactory(),
                                                                 fake_data[state.getId()])
                if state.getActionNumber():
                    category = self.__input_type[state.getActionNumber() - 1]
                else:
                    category = ""
                app_events.append(AppEvent(xpath=interactive_app_element.getXpath(),
                                           value=value, category=category))

        initial_state: State = episode_episode_handler.getState(0)
        directive = Directive(url=initial_state.getUrl(), dom=initial_state.getDOM(),
                              formXPath=target_page.getFormXPath(), appEvents=app_events, codeCoverages=code_coverages)
        target_page.appendDirective(directive=directive)
        self._target_page_repository.update(TargetPageEntityMapper.mappingTargetPageEntityFrom(targetPage=target_page))

        output.setDirectiveDTO(DirectiveDTOMapper.mappingDirectiveDTOFrom(directive=directive))
