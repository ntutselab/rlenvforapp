from RLEnvForApp.domain.environment.state.AppElement import AppElement
from RLEnvForApp.usecase.environment.state.entity.AppElementEntity import \
    AppElementEntity


def mapping_app_element_entity_from(appElement: AppElement):
    if appElement is None:
        return None
    return AppElementEntity(tagName=appElement.get_tag_name(), name=appElement.get_name(
    ), type=appElement.get_type(), xpath=appElement.get_xpath(), value=appElement.get_value())


def mapping_app_element_from(appElementEntity: AppElementEntity):
    if appElementEntity is None:
        return None
    return AppElement(tagName=appElementEntity.get_tag_name(), name=appElementEntity.get_name(
    ), type=appElementEntity.get_type(), xpath=appElementEntity.get_xpath(), value=appElementEntity.get_value())
