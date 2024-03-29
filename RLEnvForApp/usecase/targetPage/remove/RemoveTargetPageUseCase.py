from dependency_injector.wiring import Provide, inject

from configuration.di.EnvironmentDIContainers import EnvironmentDIContainers
from RLEnvForApp.usecase.repository.TargetPageRepository import TargetPageRepository

from . import RemoveTargetPageInput, RemoveTargetPageOutput


class RemoveTargetPageUseCase:
    @inject
    def __init__(self, repository: TargetPageRepository = Provide[EnvironmentDIContainers.targetPageRepository]):
        self._repository = repository

    def execute(self, input: RemoveTargetPageInput.RemoveTargetPageInput, output: RemoveTargetPageOutput.RemoveTargetPageOutput):
        self._repository.deleteById(input.getTargetPageId())

        output.setId(input.getTargetPageId())
