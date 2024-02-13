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
        target_page_id = input.get_target_page_id()
        target_page_entity = self._repository.find_by_id(target_page_id)
        target_page = TargetPageEntityMapper.mapping_target_page_from(
            target_page_entity=target_page_entity)
        target_page_dto = TargetPageDTOMapper.mapping_target_page_dto_from(
            target_page=target_page)
        output.set_target_page_dto(target_page_dto=target_page_dto)
