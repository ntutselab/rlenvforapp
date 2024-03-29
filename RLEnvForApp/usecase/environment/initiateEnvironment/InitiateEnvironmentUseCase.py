from dependency_injector.wiring import Provide, inject

from configuration.di.EnvironmentDIContainers import EnvironmentDIContainers
from RLEnvForApp.domain.environment.actionCommandFactoryService.IActionCommandFactoryService import \
    IActionCommandFactoryService
from RLEnvForApp.domain.environment.observationService.IObservationService import \
    IObservationService

from . import InitiateEnvironmentInput, InitiateEnvironmentOutput


class InitiateEnvironmentUseCase:
    @inject
    def __init__(self, actionCommandFactory: IActionCommandFactoryService = Provide[EnvironmentDIContainers.actionCommandFactory],
                 observationSerivce: IObservationService = Provide[EnvironmentDIContainers.observationService],):
        self._actionCommandFactory = actionCommandFactory
        self._observationService = observationSerivce

    def execute(self, input: InitiateEnvironmentInput.InitiateEnvironmentInput, output: InitiateEnvironmentOutput.InitiateEnvironmentOutput):
        output.setActionSpaceSize(self._actionCommandFactory.getActionSpaceSize())
        output.setObservationSize(self._observationService.getObservationSize())
        output.setActionList(self._actionCommandFactory.getActionList())
