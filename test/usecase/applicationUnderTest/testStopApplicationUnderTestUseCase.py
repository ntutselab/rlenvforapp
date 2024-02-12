import unittest
from test.usecase.HirerarchyInitial import HirerarchyInitial

import requests

from RLEnvForApp.adapter.applicationUnderTest.DockerServerHandler import \
    DockerServerHandler
from RLEnvForApp.adapter.repository.applicationUnderTest.InMemoryApplicationUnderTestRepository import \
    InMemoryApplicationUnderTestRepository
from RLEnvForApp.usecase.applicationUnderTest.stop import (
    StopApplicationUnderTestInput, StopApplicationUnderTestOutput,
    StopApplicationUnderTestUseCase)


class testStopApplicationUnderTestUseCase(unittest.TestCase):
    def set_up(self) -> None:
        self._autRepository = InMemoryApplicationUnderTestRepository()
        self._applicationHandler = DockerServerHandler(
            "RLEnvForApp/application/serverInstance")
        self._hirerarchyInitial = HirerarchyInitial(
            autRepository=self._autRepository,
            applicationHandler=self._applicationHandler)

    def test_stop_application_under_testing(self):
        self._hirerarchyInitial.start_aut_server(
            applicationName="timeoff_management_with_coverage")

        autEntity = self._autRepository.find_all()[0]
        stopAUTUseCase = StopApplicationUnderTestUseCase.StopApplicationUnderTestUseCase(
            repository=self._autRepository, applicationHandler=self._applicationHandler)
        stopAUTInput = StopApplicationUnderTestInput.StopApplicationUnderTestInput(
            id=autEntity.get_id())
        stopAUTOutput = StopApplicationUnderTestOutput.StopApplicationUnderTestOutput()
        stopAUTUseCase.execute(stopAUTInput, stopAUTOutput)

        isAUTAvailable = True
        try:
            requests.get(stopAUTOutput.get_url())
        except requests.exceptions.ConnectionError:
            isAUTAvailable = False

        self.assertEqual(False, isAUTAvailable)
