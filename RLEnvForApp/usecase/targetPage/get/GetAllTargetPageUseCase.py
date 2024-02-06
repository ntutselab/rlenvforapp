from dependency_injector.wiring import Provide, inject

from configuration.di.EnvironmentDIContainers import EnvironmentDIContainers
from . import (GetAllTargetPageInput, GetAllTargetPageOutput)
from ..dto.TargetPageDTO import TargetPageDTO
from ..mapper import TargetPageEntityMapper, TargetPageDTOMapper
from ...repository.TargetPageRepository import TargetPageRepository

class GetAllTargetPageUseCase:
    @inject
    def __init__(self, repository: TargetPageRepository = Provide[EnvironmentDIContainers.targetPageRepository]):
        self._repository = repository

    def execute(self, input: GetAllTargetPageInput, output: GetAllTargetPageOutput):
        targetPageDTOs: [TargetPageDTO] = []
        targetPageEntities = self._repository.findAll()
        for targetPageEntity in targetPageEntities:
            targetPage = TargetPageEntityMapper.mappingTargetPageFrom(targetPageEntity=targetPageEntity)
            targetPageDTO = TargetPageDTOMapper.mappingTargetPageDTOFrom(targetPage=targetPage)
            targetPageDTOs.append(targetPageDTO)
        output.setTargetPageDTOs(targetPageDTOs=targetPageDTOs)
