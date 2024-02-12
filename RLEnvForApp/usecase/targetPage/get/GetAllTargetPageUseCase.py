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
        targetPageDTOs: [TargetPageDTO] = []
        targetPageEntities = self._repository.find_all()
        for targetPageEntity in targetPageEntities:
            targetPage = TargetPageEntityMapper.mapping_target_page_from(
                targetPageEntity=targetPageEntity)
            targetPageDTO = TargetPageDTOMapper.mapping_target_page_dto_from(
                targetPage=targetPage)
            targetPageDTOs.append(targetPageDTO)
        output.set_target_page_dt_os(targetPageDTOs=targetPageDTOs)
