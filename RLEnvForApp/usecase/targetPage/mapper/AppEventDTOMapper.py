from RLEnvForApp.domain.targetPage.AppEvent import AppEvent
from RLEnvForApp.usecase.targetPage.dto.AppEventDTO import AppEventDTO


def mapping_app_event_from(appEventDTO: AppEventDTO):
    appEvent = AppEvent(
        xpath=appEventDTO.get_xpath(),
        value=appEventDTO.get_value(),
        category=appEventDTO.get_category())
    return appEvent


def mapping_app_event_dto_from(appEvent: AppEvent):
    appEventDTO = AppEventDTO(
        xpath=appEvent.get_xpath(),
        value=appEvent.get_value(),
        category=appEvent.get_category())
    return appEventDTO
