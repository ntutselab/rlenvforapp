from RLEnvForApp.domain.targetPage.AppEvent import AppEvent
from RLEnvForApp.usecase.targetPage.dto.AppEventDTO import AppEventDTO


def mapping_app_event_from(app_event_dto: AppEventDTO):
    app_event = AppEvent(
        xpath=app_event_dto.get_xpath(),
        value=app_event_dto.get_value(),
        category=app_event_dto.get_category())
    return app_event


def mapping_app_event_dto_from(app_event: AppEvent):
    app_event_dto = AppEventDTO(
        xpath=app_event.get_xpath(),
        value=app_event.get_value(),
        category=app_event.get_category())
    return app_event_dto
