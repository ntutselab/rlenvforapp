import unittest

from configuration.di.EnvironmentDIContainers import EnvironmentDIContainers
from RLEnvForApp.domain.environment.observationService.DefaultForTestObservationService import \
    DefaultForTestObservationService
from RLEnvForApp.usecase.environment.initiateEnvironment import (
    InitiateEnvironmentInput, InitiateEnvironmentOutput,
    InitiateEnvironmentUseCase)


class testInitiateEnvironmentUseCase(unittest.TestCase):
    def set_up(self) -> None:
        container = EnvironmentDIContainers()
        container.config.from_ini("configuration/config/default.ini")
        container.wire(modules=[InitiateEnvironmentUseCase])

    def test_initiate_environment(self):
        initiate_environment_use_case = InitiateEnvironmentUseCase.InitiateEnvironmentUseCase(
            observationSerivce=DefaultForTestObservationService())
        initiate_environment_input = InitiateEnvironmentInput.InitiateEnvironmentInput()
        initiate_environment_output = InitiateEnvironmentOutput.InitiateEnvironmentOutput()

        initiate_environment_use_case.execute(
            input=initiate_environment_input,
            output=initiate_environment_output)
        self.assertEqual(
            (1, 150, 1), initiate_environment_output.get_observation_size())
        self.assertEqual(8, initiate_environment_output.get_action_space_size())
