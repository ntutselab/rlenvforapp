
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
        self._directiveRuleService: IDirectiveRuleService = directiveRuleService
        self._targetPageRepository = targetPageRepository
        self._episodeHandlerRepository = episodeHandlerRepository

    def execute(self, input: CreateDirectiveInput.CreateDirectiveInput,
                output: CreateDirectiveOutput.CreateDirectiveOutput):
        targetPageEntity = self._targetPageRepository.find_by_id(
            input.get_target_page_id())
        targetPage = TargetPageEntityMapper.mapping_target_page_from(
            targetPageEntity=targetPageEntity)
        targetEpisodeHandlerEntity = self._episodeHandlerRepository.find_by_id(
            input.get_episode_handler_id())
        episodeEpisodeHandler = EpisodeHandlerEntityMapper.mapping_episode_handler_form(
            targetEpisodeHandlerEntity)
        codeCoverages: [CodeCoverage] = None
        appEvents: [AppEvent] = []

        fileManager = FileManager()
        fileManager.create_folder("output", "create")

        for state in episodeEpisodeHandler.get_all_state():
            actionType = state.get_action_type()
            interactiveAppElement: AppElement = state.get_interacted_element()
            codeCoverages = state.get_code_coverages()

            if (interactiveAppElement is None):
                continue

            if actionType == "changeFocus":
                continue
            if actionType == "click":
                if not interactiveAppElement.get_tag_name() == "button" and not (interactiveAppElement.get_tag_name() == "input" and (interactiveAppElement.get_type() ==
                                                                                                                                  "submit" or interactiveAppElement.get_type() == "button" or interactiveAppElement.get_type() == "image" or interactiveAppElement.get_type() == "checkbox")):
                    continue
                appEvents.append(
                    AppEvent(
                        xpath=interactiveAppElement.get_xpath(),
                        value="",
                        category="click"))
            if actionType == "input":
                if not interactiveAppElement.get_tag_name(
                ) == "input" and not interactiveAppElement.get_tag_name() == "textarea":
                    continue
                value = state.get_app_event_input_value()
                if state.get_action_number():
                    category = inputTypes[state.get_action_number()]
                else:
                    category = ""
                appEvents.append(
                    AppEvent(
                        xpath=interactiveAppElement.get_xpath(),
                        value=value,
                        category=category))

        initialState: State = episodeEpisodeHandler.get_state(0)
        directive = Directive(
            url=initialState.get_url(),
            dom=initialState.get_dom(),
            formXPath=targetPage.get_form_x_path(),
            appEvents=appEvents,
            codeCoverages=codeCoverages)
        targetPage.append_directive(directive=directive)
        self._targetPageRepository.update(
            TargetPageEntityMapper.mapping_target_page_entity_from(
                targetPage=targetPage))

        output.set_directive_dto(
            DirectiveDTOMapper.mapping_directive_dto_from(
                directive=directive))
