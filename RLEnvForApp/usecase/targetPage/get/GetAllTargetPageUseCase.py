from dependency_injector.wiring import Provide, inject

from configuration.di.EnvironmentDIContainers import EnvironmentDIContainers

from ...repository.TargetPageRepository import TargetPageRepository
from ..dto.TargetPageDTO import TargetPageDTO
from ..mapper import TargetPageDTOMapper, TargetPageEntityMapper
from . import GetAllTargetPageInput, GetAllTargetPageOutput


class GetAllTargetPageUseCase:
    @inject
    def __init__(
            self, repository: TargetPageRepository = Provide[EnvironmentDIContainers.targetPageRepository]):
        self._repository = repository

    def execute(self, input: GetAllTargetPageInput,
                output: GetAllTargetPageOutput):
        target_page_dt_os: [TargetPageDTO] = []
        target_page_entities = self._repository.find_all()
        for target_page_entity in target_page_entities:
            target_page = TargetPageEntityMapper.mapping_target_page_from(
                target_page_entity=target_page_entity)
            target_page_dto = TargetPageDTOMapper.mapping_target_page_dto_from(
                target_page=target_page)
            target_page_dt_os.append(target_page_dto)
        output.set_target_page_dt_os(target_page_dt_os=target_page_dt_os)
