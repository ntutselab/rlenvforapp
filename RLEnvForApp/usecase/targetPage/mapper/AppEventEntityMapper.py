from RLEnvForApp.domain.targetPage.AppEvent import AppEvent
from RLEnvForApp.usecase.targetPage.entity.AppEventEntity import AppEventEntity


def mapping_app_event_from(appEventEntity: AppEventEntity):
    appEvent = AppEvent(xpath=appEventEntity.get_xpath(), value=appEventEntity.get_value(),
                        category=appEventEntity.get_category())
    return appEvent


def mapping_app_event_entity_from(appEvent: AppEvent):
    appEventEntity = AppEventEntity(xpath=appEvent.get_xpath(), value=appEvent.get_value(),
                                    category=appEvent.get_category())
    return appEventEntity
