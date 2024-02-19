from RLEnvForApp.usecase.repository import TargetPageRepository
from RLEnvForApp.usecase.targetPage.create import (CreateTargetPageInput, CreateTargetPageOutput,
                                                   CreateTargetPageUseCase)
from RLEnvForApp.usecase.targetPage.dto.AppEventDTO import AppEventDTO


class TargetPageHierarchyInitial:
    def __init__(self):
        pass

    def createTargetPage(self, targetPageRepository: TargetPageRepository.TargetPageRepository, targetPageUrl: str, rootUrl: str, appEventDTOs: [AppEventDTO]):
        createTargetPageUseCase = CreateTargetPageUseCase.CreateTargetPageUseCase(
            repository=targetPageRepository)
        createTargetPageInput = CreateTargetPageInput.CreateTargetPageInput(targetPageUrl=targetPageUrl,
                                                                            rootUrl=rootUrl,
                                                                            appEventDTOs=appEventDTOs)
        createTargetPageOutput = CreateTargetPageOutput.CreateTargetPageOutput()
        createTargetPageUseCase.execute(createTargetPageInput, createTargetPageOutput)

        return createTargetPageOutput.getId()
