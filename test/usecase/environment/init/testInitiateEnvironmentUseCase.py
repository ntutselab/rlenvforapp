import unittest

from configuration.di.EnvironmentDIContainers import EnvironmentDIContainers
from RLEnvForApp.domain.environment.observationService.DefaultForTestObservationService import \
    DefaultForTestObservationService
from RLEnvForApp.usecase.environment.initiateEnvironment import (
    InitiateEnvironmentInput, InitiateEnvironmentOutput,
    InitiateEnvironmentUseCase)


class testInitiateEnvironmentUseCase(unittest.TestCase):
    def setUp(self) -> None:
        container = EnvironmentDIContainers()
        container.config.from_ini("configuration/config/default.ini")
        container.wire(modules=[InitiateEnvironmentUseCase])

    def test_initiate_environment(self):
        initiateEnvironmentUseCase = InitiateEnvironmentUseCase.InitiateEnvironmentUseCase(
            observationSerivce=DefaultForTestObservationService())
        initiateEnvironmentInput = InitiateEnvironmentInput.InitiateEnvironmentInput()
        initiateEnvironmentOutput = InitiateEnvironmentOutput.InitiateEnvironmentOutput()

        initiateEnvironmentUseCase.execute(
            input=initiateEnvironmentInput,
            output=initiateEnvironmentOutput)
        self.assertEqual((1, 150, 1), initiateEnvironmentOutput.getObservationSize())
        self.assertEqual(8, initiateEnvironmentOutput.getActionSpaceSize())
