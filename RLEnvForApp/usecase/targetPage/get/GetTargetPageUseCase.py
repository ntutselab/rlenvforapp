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
        targetPageId = input.getTargetPageId()
        targetPageEntity = self._repository.findById(targetPageId)
        targetPage = TargetPageEntityMapper.mappingTargetPageFrom(targetPageEntity=targetPageEntity)
        targetPageDTO = TargetPageDTOMapper.mappingTargetPageDTOFrom(targetPage=targetPage)
        output.setTargetPageDTO(targetPageDTO=targetPageDTO)
