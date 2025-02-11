from RLEnvForApp.domain.environment.state import AppElement
from RLEnvForApp.usecase.environment.autOperator.dto.AppElementDTO import AppElementDTO


def mappingAppElementFrom(appElementDTO: AppElementDTO) -> AppElement.AppElement:
    if appElementDTO is None:
        return None
    return AppElement.AppElement(tagName=appElementDTO.getTagName(), name=appElementDTO.getName(),
                                 type=appElementDTO.getType(), placeholder=appElementDTO.getPlaceholder(),
                                 label=appElementDTO.getLabel(), xpath=appElementDTO.getXpath(),
                                 value=appElementDTO.getValue())


def mappingAppElementDTOFrom(appElement: AppElement.AppElement) -> AppElementDTO:
    if appElement is None:
        return None
    return AppElementDTO(tagName=appElement.getTagName(), name=appElement.getName(),
                         type=appElement.getType(), placeholder=appElement.getPlaceholder(),
                         label=appElement.getLabel(), xpath=appElement.getXpath(),
                         value=appElement.getValue())
