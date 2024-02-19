import unittest
from test.usecase.HirerarchyInitial import HirerarchyInitial

import requests

from RLEnvForApp.adapter.applicationUnderTest.DockerServerHandler import DockerServerHandler
from RLEnvForApp.adapter.repository.applicationUnderTest.InMemoryApplicationUnderTestRepository import \
    InMemoryApplicationUnderTestRepository
from RLEnvForApp.usecase.applicationUnderTest.stop import (StopApplicationUnderTestInput,
                                                           StopApplicationUnderTestOutput,
                                                           StopApplicationUnderTestUseCase)


class testStopApplicationUnderTestUseCase(unittest.TestCase):
    def setUp(self) -> None:
        self._autRepository = InMemoryApplicationUnderTestRepository()
        self._applicationHandler = DockerServerHandler("RLEnvForApp/application/serverInstance")
        self._hirerarchyInitial = HirerarchyInitial(
            autRepository=self._autRepository, applicationHandler=self._applicationHandler)

    def test_stop_application_under_testing(self):
        self._hirerarchyInitial.startAUTServer(applicationName="timeoff_management_with_coverage")

        autEntity = self._autRepository.findAll()[0]
        stopAUTUseCase = StopApplicationUnderTestUseCase.StopApplicationUnderTestUseCase(
            repository=self._autRepository, applicationHandler=self._applicationHandler)
        stopAUTInput = StopApplicationUnderTestInput.StopApplicationUnderTestInput(
            id=autEntity.getId())
        stopAUTOutput = StopApplicationUnderTestOutput.StopApplicationUnderTestOutput()
        stopAUTUseCase.execute(stopAUTInput, stopAUTOutput)

        isAUTAvailable = True
        try:
            requests.get(stopAUTOutput.getUrl())
        except requests.exceptions.ConnectionError:
            isAUTAvailable = False

        self.assertEqual(False, isAUTAvailable)
