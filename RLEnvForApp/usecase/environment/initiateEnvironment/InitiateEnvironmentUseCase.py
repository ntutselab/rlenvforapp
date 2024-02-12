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

    def execute(self, input: InitiateEnvironmentInput.InitiateEnvironmentInput,
                output: InitiateEnvironmentOutput.InitiateEnvironmentOutput):
        output.set_action_space_size(
            self._actionCommandFactory.get_action_space_size())
        output.set_observation_size(
            self._observationService.get_observation_size())
        output.set_action_list(self._actionCommandFactory.get_action_list())
