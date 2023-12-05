from RLEnvForApp.domain.environment.state.AppElement import AppElement
from RLEnvForApp.usecase.environment.state.entity.AppElementEntity import AppElementEntity


def mappingAppElementEntityFrom(appElement: AppElement):
    if appElement is None:
        return None
    return AppElementEntity(tagName=appElement.getTagName(), name=appElement.getName(), type=appElement.getType(), xpath=appElement.getXpath(), value=appElement.getValue())


def mappingAppElementFrom(appElementEntity: AppElementEntity):
    if appElementEntity is None:
        return None
    return AppElement(tagName=appElementEntity.getTagName(), name=appElementEntity.getName(), type=appElementEntity.getType(), xpath=appElementEntity.getXpath(), value=appElementEntity.getValue())
