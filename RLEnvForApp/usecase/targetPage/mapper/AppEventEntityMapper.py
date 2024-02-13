from RLEnvForApp.domain.targetPage.AppEvent import AppEvent
from RLEnvForApp.usecase.targetPage.entity.AppEventEntity import AppEventEntity


def mapping_app_event_from(app_event_entity: AppEventEntity):
    app_event = AppEvent(xpath=app_event_entity.get_xpath(), value=app_event_entity.get_value(),
                        category=app_event_entity.get_category())
    return app_event


def mapping_app_event_entity_from(app_event: AppEvent):
    app_event_entity = AppEventEntity(xpath=app_event.get_xpath(), value=app_event.get_value(),
                                    category=app_event.get_category())
    return app_event_entity
