# GetTargetPage
from dependency_injector.wiring import Provide, inject

from configuration.di.EnvironmentDIContainers import EnvironmentDIContainers

from ...repository.TargetPageRepository import TargetPageRepository
from ..mapper import TargetPageDTOMapper, TargetPageEntityMapper
from . import GetTargetPageInput, GetTargetPageOutput


class GetTargetPageUseCase:
    @inject
    def __init__(
            self, repository: TargetPageRepository = Provide[EnvironmentDIContainers.targetPageRepository]):
        self._repository = repository

    def execute(self, input: GetTargetPageInput, output: GetTargetPageOutput):
        targetPageId = input.get_target_page_id()
        targetPageEntity = self._repository.find_by_id(targetPageId)
        targetPage = TargetPageEntityMapper.mapping_target_page_from(
            targetPageEntity=targetPageEntity)
        targetPageDTO = TargetPageDTOMapper.mapping_target_page_dto_from(
            targetPage=targetPage)
        output.set_target_page_dto(targetPageDTO=targetPageDTO)
