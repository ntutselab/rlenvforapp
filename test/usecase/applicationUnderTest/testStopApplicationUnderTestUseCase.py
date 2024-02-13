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


class TestStopApplicationUnderTestUseCase(unittest.TestCase):
    def set_up(self) -> None:
        self._aut_repository = InMemoryApplicationUnderTestRepository()
        self._application_handler = DockerServerHandler(
            "RLEnvForApp/application/serverInstance")
        self._hirerarchy_initial = HirerarchyInitial(
            autRepository=self._aut_repository,
            applicationHandler=self._application_handler)

    def test_stop_application_under_testing(self):
        self._hirerarchy_initial.start_aut_server(
            applicationName="timeoff_management_with_coverage")

        aut_entity = self._aut_repository.find_all()[0]
        stop_aut_use_case = StopApplicationUnderTestUseCase.StopApplicationUnderTestUseCase(
            repository=self._aut_repository, applicationHandler=self._application_handler)
        stop_aut_input = StopApplicationUnderTestInput.StopApplicationUnderTestInput(
            id=aut_entity.get_id())
        stop_aut_output = StopApplicationUnderTestOutput.StopApplicationUnderTestOutput()
        stop_aut_use_case.execute(stop_aut_input, stop_aut_output)

        is_aut_available = True
        try:
            requests.get(stop_aut_output.get_url())
        except requests.exceptions.ConnectionError:
            is_aut_available = False

        self.assertEqual(False, is_aut_available)
