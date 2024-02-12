from RLEnvForApp.domain.environment.state import AppElement
from RLEnvForApp.usecase.environment.autOperator.dto.AppElementDTO import \
    AppElementDTO


def mapping_app_element_from(
        appElementDTO: AppElementDTO) -> AppElement.AppElement:
    if appElementDTO is None:
        return None
    return AppElement.AppElement(tagName=appElementDTO.get_tag_name(), name=appElementDTO.get_name(),
                                 type=appElementDTO.get_type(), xpath=appElementDTO.get_xpath(),
                                 value=appElementDTO.get_value())


def mapping_app_element_dto_from(
        appElement: AppElement.AppElement) -> AppElementDTO:
    if appElement is None:
        return None
    return AppElementDTO(tagName=appElement.get_tag_name(), name=appElement.get_name(), type=appElement.get_type(),
                         xpath=appElement.get_xpath(), value=appElement.get_value())
