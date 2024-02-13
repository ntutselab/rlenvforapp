
from dependency_injector.wiring import Provide, inject

from configuration.di.EnvironmentDIContainers import EnvironmentDIContainers
from RLEnvForApp.adapter.targetPagePort.FileManager import FileManager
from RLEnvForApp.domain.environment.inputSpace import inputTypes
from RLEnvForApp.domain.environment.state.AppElement import AppElement
from RLEnvForApp.domain.environment.state.CodeCoverage import CodeCoverage
from RLEnvForApp.domain.environment.state.State import State
from RLEnvForApp.domain.targetPage.AppEvent import AppEvent
from RLEnvForApp.domain.targetPage.Directive import Directive
from RLEnvForApp.domain.targetPage.DirectiveRuleService.IDirectiveRuleService import \
    IDirectiveRuleService
from RLEnvForApp.usecase.environment.episodeHandler.mapper import \
    EpisodeHandlerEntityMapper
from RLEnvForApp.usecase.repository.EpisodeHandlerRepository import \
    EpisodeHandlerRepository
from RLEnvForApp.usecase.repository.TargetPageRepository import \
    TargetPageRepository
from RLEnvForApp.usecase.targetPage.create import (CreateDirectiveInput,
                                                   CreateDirectiveOutput)
from RLEnvForApp.usecase.targetPage.mapper import (DirectiveDTOMapper,
                                                   TargetPageEntityMapper)


class CreateDirectiveUseCase:
    @inject
    def __init__(self,
                 targetPageRepository: TargetPageRepository = Provide[
                     EnvironmentDIContainers.targetPageRepository],
                 episodeHandlerRepository: EpisodeHandlerRepository = Provide[
                     EnvironmentDIContainers.episodeHandlerRepository],
                 directiveRuleService: IDirectiveRuleService = Provide[EnvironmentDIContainers.directiveRuleService]):
        self._directive_rule_service: IDirectiveRuleService = directiveRuleService
        self._target_page_repository = targetPageRepository
        self._episode_handler_repository = episodeHandlerRepository

    def execute(self, input: CreateDirectiveInput.CreateDirectiveInput,
                output: CreateDirectiveOutput.CreateDirectiveOutput):
        target_page_entity = self._target_page_repository.find_by_id(
            input.get_target_page_id())
        target_page = TargetPageEntityMapper.mapping_target_page_from(
            target_page_entity=target_page_entity)
        target_episode_handler_entity = self._episode_handler_repository.find_by_id(
            input.get_episode_handler_id())
        episode_episode_handler = EpisodeHandlerEntityMapper.mapping_episode_handler_form(
            target_episode_handler_entity)
        code_coverages: [CodeCoverage] = None
        app_events: [AppEvent] = []

        file_manager = FileManager()
        file_manager.create_folder("output", "create")

        for state in episode_episode_handler.get_all_state():
            action_type = state.get_action_type()
            interactiveAppElement: AppElement = state.get_interacted_element()
            code_coverages = state.get_code_coverages()

            if (interactiveAppElement is None):
                continue

            if action_type == "changeFocus":
                continue
            if action_type == "click":
                if not interactiveAppElement.get_tag_name() == "button" and not (interactiveAppElement.get_tag_name() == "input" and (interactiveAppElement.get_type() ==
                                                                                                                                  "submit" or interactiveAppElement.get_type() == "button" or interactiveAppElement.get_type() == "image" or interactiveAppElement.get_type() == "checkbox")):
                    continue
                app_events.append(
                    AppEvent(
                        xpath=interactiveAppElement.get_xpath(),
                        value="",
                        category="click"))
            if action_type == "input":
                if not interactiveAppElement.get_tag_name(
                ) == "input" and not interactiveAppElement.get_tag_name() == "textarea":
                    continue
                value = state.get_app_event_input_value()
                if state.get_action_number():
                    category = inputTypes[state.get_action_number()]
                else:
                    category = ""
                app_events.append(
                    AppEvent(
                        xpath=interactiveAppElement.get_xpath(),
                        value=value,
                        category=category))

        initial_state: State = episode_episode_handler.get_state(0)
        directive = Directive(
            url=initial_state.get_url(),
            dom=initial_state.get_dom(),
            form_x_path=target_page.get_form_x_path(),
            app_events=app_events,
            code_coverages=code_coverages)
        target_page.append_directive(directive=directive)
        self._target_page_repository.update(
            TargetPageEntityMapper.mapping_target_page_entity_from(
                target_page=target_page))

        output.set_directive_dto(
            DirectiveDTOMapper.mapping_directive_dto_from(
                directive=directive))
