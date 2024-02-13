from RLEnvForApp.domain.environment.state.AppElement import AppElement
from RLEnvForApp.usecase.environment.state.entity.AppElementEntity import \
    AppElementEntity


def mapping_app_element_entity_from(app_element: AppElement):
    if app_element is None:
        return None
    return AppElementEntity(tag_name=app_element.get_tag_name(), name=app_element.get_name(
    ), type=app_element.get_type(), xpath=app_element.get_xpath(), value=app_element.get_value())


def mapping_app_element_from(app_element_entity: AppElementEntity):
    if app_element_entity is None:
        return None
    return AppElement(tag_name=app_element_entity.get_tag_name(), name=app_element_entity.get_name(
    ), type=app_element_entity.get_type(), xpath=app_element_entity.get_xpath(), value=app_element_entity.get_value())
