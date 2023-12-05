from RLEnvForApp.domain.targetPage.AppEvent import AppEvent
from RLEnvForApp.usecase.targetPage.entity.AppEventEntity import AppEventEntity


def mappingAppEventFrom(appEventEntity: AppEventEntity):
    appEvent = AppEvent(xpath=appEventEntity.getXpath(), value=appEventEntity.getValue(),
                        category=appEventEntity.getCategory())
    return appEvent


def mappingAppEventEntityFrom(appEvent: AppEvent):
    appEventEntity = AppEventEntity(xpath=appEvent.getXpath(), value=appEvent.getValue(),
                                    category=appEvent.getCategory())
    return appEventEntity
