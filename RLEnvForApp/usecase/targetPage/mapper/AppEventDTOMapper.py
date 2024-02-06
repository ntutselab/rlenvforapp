from RLEnvForApp.domain.targetPage.AppEvent import AppEvent
from RLEnvForApp.usecase.targetPage.dto.AppEventDTO import AppEventDTO


def mappingAppEventFrom(appEventDTO: AppEventDTO):
    appEvent = AppEvent(
        xpath=appEventDTO.getXpath(),
        value=appEventDTO.getValue(),
        category=appEventDTO.getCategory())
    return appEvent


def mappingAppEventDTOFrom(appEvent: AppEvent):
    appEventDTO = AppEventDTO(
        xpath=appEvent.getXpath(),
        value=appEvent.getValue(),
        category=appEvent.getCategory())
    return appEventDTO
