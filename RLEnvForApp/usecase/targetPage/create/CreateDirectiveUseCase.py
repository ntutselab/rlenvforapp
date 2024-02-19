
from RLEnvForApp.adapter.targetPagePort.FileManager import FileManager
from RLEnvForApp.domain.environment.inputSpace import inputTypes
from RLEnvForApp.domain.environment.state.AppElement import AppElement
from RLEnvForApp.domain.environment.state.CodeCoverage import CodeCoverage
from RLEnvForApp.domain.environment.state.State import State
from RLEnvForApp.domain.targetPage.AppEvent import AppEvent
from RLEnvForApp.domain.targetPage.Directive import Directive
from RLEnvForApp.domain.targetPage.DirectiveRuleService.IDirectiveRuleService import IDirectiveRuleService
from RLEnvForApp.usecase.environment.episodeHandler.mapper import EpisodeHandlerEntityMapper
from RLEnvForApp.usecase.repository.EpisodeHandlerRepository import EpisodeHandlerRepository
from RLEnvForApp.usecase.repository.TargetPageRepository import TargetPageRepository
from RLEnvForApp.usecase.targetPage.create import (CreateDirectiveInput, CreateDirectiveOutput)
from RLEnvForApp.usecase.targetPage.mapper import TargetPageEntityMapper, DirectiveDTOMapper
from configuration.di.EnvironmentDIContainers import EnvironmentDIContainers
from dependency_injector.wiring import inject, Provide

class CreateDirectiveUseCase:
    @inject
    def __init__(self,
                 targetPageRepository: TargetPageRepository = Provide[EnvironmentDIContainers.targetPageRepository],
                 episodeHandlerRepository: EpisodeHandlerRepository = Provide[EnvironmentDIContainers.episodeHandlerRepository],
                 directiveRuleService: IDirectiveRuleService = Provide[EnvironmentDIContainers.directiveRuleService]):
        self._directiveRuleService: IDirectiveRuleService = directiveRuleService
        self._targetPageRepository = targetPageRepository
        self._episodeHandlerRepository = episodeHandlerRepository

    def execute(self, input: CreateDirectiveInput.CreateDirectiveInput,
                output: CreateDirectiveOutput.CreateDirectiveOutput):
        targetPageEntity = self._targetPageRepository.findById(input.getTargetPageId())
        targetPage = TargetPageEntityMapper.mappingTargetPageFrom(targetPageEntity=targetPageEntity)
        targetEpisodeHandlerEntity = self._episodeHandlerRepository.findById(input.getEpisodeHandlerId())
        episodeEpisodeHandler = EpisodeHandlerEntityMapper.mappingEpisodeHandlerForm(targetEpisodeHandlerEntity)
        codeCoverages: [CodeCoverage] = None
        appEvents: [AppEvent] = []

        fileManager = FileManager()
        fileManager.createFolder("output", "create")

        for state in episodeEpisodeHandler.getAllState():
            actionType = state.getActionType()
            interactiveAppElement: AppElement = state.getInteractedElement()
            codeCoverages = state.getCodeCoverages()

            if interactiveAppElement is None:
                continue

            if actionType == "changeFocus":
                continue
            if actionType == "click":
                if not interactiveAppElement.getTagName() == "button" and not (interactiveAppElement.getTagName() == "input" and (interactiveAppElement.getType() == "submit" or interactiveAppElement.getType() == "button" or interactiveAppElement.getType() == "image" or interactiveAppElement.getType() == "checkbox")):
                    continue
                appEvents.append(AppEvent(xpath=interactiveAppElement.getXpath(), value="", category="click"))
            if actionType == "input":
                if not interactiveAppElement.getTagName() == "input" and not interactiveAppElement.getTagName() == "textarea":
                    continue
                value = state.getAppEventInputValue()
                if state.getActionNumber():
                    category = inputTypes[state.getActionNumber()]
                else:
                    category = ""
                appEvents.append(AppEvent(xpath=interactiveAppElement.getXpath(), value=value, category=category))

        initialState: State = episodeEpisodeHandler.getState(0)
        directive = Directive(url=initialState.getUrl(), dom=initialState.getDOM(), formXPath=targetPage.getFormXPath(), appEvents=appEvents, codeCoverages=codeCoverages)
        targetPage.appendDirective(directive=directive)
        self._targetPageRepository.update(TargetPageEntityMapper.mappingTargetPageEntityFrom(targetPage=targetPage))

        output.setDirectiveDTO(DirectiveDTOMapper.mappingDirectiveDTOFrom(directive=directive))
