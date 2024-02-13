from RLEnvForApp.domain.environment.state import AppElement
from RLEnvForApp.usecase.environment.autOperator.dto.AppElementDTO import \
    AppElementDTO


def mapping_app_element_from(
        app_element_dto: AppElementDTO) -> AppElement.AppElement:
    if app_element_dto is None:
        return None
    return AppElement.AppElement(tag_name=app_element_dto.get_tag_name(), name=app_element_dto.get_name(),
                                 type=app_element_dto.get_type(), xpath=app_element_dto.get_xpath(),
                                 value=app_element_dto.get_value())


def mapping_app_element_dto_from(
        app_element: AppElement.AppElement) -> AppElementDTO:
    if app_element is None:
        return None
    return AppElementDTO(tag_name=app_element.get_tag_name(), name=app_element.get_name(), type=app_element.get_type(),
                         xpath=app_element.get_xpath(), value=app_element.get_value())
