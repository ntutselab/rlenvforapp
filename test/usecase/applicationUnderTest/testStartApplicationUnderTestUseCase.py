from test.usecase.HirerarchyInitial import HirerarchyInitial
from unittest import TestCase

import requests

from RLEnvForApp.adapter.applicationUnderTest.DockerServerHandler import \
    DockerServerHandler
from RLEnvForApp.adapter.repository.applicationUnderTest.InMemoryApplicationUnderTestRepository import \
    InMemoryApplicationUnderTestRepository
from RLEnvForApp.domain.applicationUnderTest.ApplicationUnderTest import \
    ApplicationUnderTest
from RLEnvForApp.usecase.applicationUnderTest.entity.ApplicationUnderTestEntity import \
    ApplicationUnderTestEntity
from RLEnvForApp.usecase.applicationUnderTest.mapper import \
    ApplicationUnderTestMapper
from RLEnvForApp.usecase.applicationUnderTest.start import (
    StartApplicationUnderTestInput, StartApplicationUnderTestOutput,
    StartApplicationUnderTestUserCase)


class testStartApplicationUnderTestUserCase(TestCase):
    def set_up(self) -> None:
        self._aut_repository = InMemoryApplicationUnderTestRepository()
        self._application_handler = DockerServerHandler(
            "RLEnvForApp/application/serverInstance")
        self._hirerarchy_initial = HirerarchyInitial(
            autRepository=self._aut_repository,
            applicationHandler=self._application_handler)

    # def tearDown(self) -> None:
    #     for autEntity in self._autRepository.findAll():
    #         self._hirerarchyInitial.stopAUTServer(autEntity.getId())

    def test_start_timeoff_management_application_under_test(self):
        self._execute_use_case_and_wait(
            applicationName="timeoff_management_with_coverage")

    def test_start_nodebb_application_under_test(self):
        self._execute_use_case_and_wait(applicationName="nodebb_with_coverage")

    def test_start_keystonejs_application_under_test(self):
        self._execute_use_case_and_wait(applicationName="keystonejs_with_coverage")

    def test_start_wagtail_application_under_test(self):
        self._execute_use_case_and_wait(applicationName="wagtails_with_coverage")

    def test_kill_busy_process(self):
        start_aut_use_case = StartApplicationUnderTestUserCase.StartApplicationUnderTestUserCase(
            repository=self._aut_repository,
            applicationHandler=DockerServerHandler("RLEnvForApp/application/serverInstance"))
        start_aut_input = StartApplicationUnderTestInput.StartApplicationUnderTestInput(
            applicationName="timeoff_management_with_coverage", ip="127.0.0.1", port=3000)
        start_aut_output = StartApplicationUnderTestOutput.StartApplicationUnderTestOutput()
        start_aut_use_case.execute(start_aut_input, start_aut_output)

        aut_entity: ApplicationUnderTestEntity = self._aut_repository.find_by_id(
            start_aut_output.get_id())
        aut: ApplicationUnderTest = ApplicationUnderTestMapper.mapping_application_under_test_from(
            aut_entity)
        self.assertEqual(aut.get_id(), start_aut_output.get_id())
        server_response = requests.get(start_aut_output.get_url())
        self.assertEqual(200, server_response.status_code)

        start_aut_use_case = StartApplicationUnderTestUserCase.StartApplicationUnderTestUserCase(
            repository=self._aut_repository,
            applicationHandler=DockerServerHandler("RLEnvForApp/application/serverInstance"))
        start_aut_input = StartApplicationUnderTestInput.StartApplicationUnderTestInput(
            applicationName="timeoff_management_with_coverage", ip="127.0.0.1", port=3000)
        start_aut_output = StartApplicationUnderTestOutput.StartApplicationUnderTestOutput()
        start_aut_use_case.execute(start_aut_input, start_aut_output)

        aut_entity: ApplicationUnderTestEntity = self._aut_repository.find_by_id(
            start_aut_output.get_id())
        aut: ApplicationUnderTest = ApplicationUnderTestMapper.mapping_application_under_test_from(
            aut_entity)
        self.assertEqual(aut.get_id(), start_aut_output.get_id())
        server_response = requests.get(start_aut_output.get_url())
        self.assertEqual(200, server_response.status_code)

        start_aut_use_case = StartApplicationUnderTestUserCase.StartApplicationUnderTestUserCase(
            repository=self._aut_repository,
            applicationHandler=DockerServerHandler("RLEnvForApp/application/serverInstance"))
        start_aut_input = StartApplicationUnderTestInput.StartApplicationUnderTestInput(
            applicationName="nodebb_with_coverage", ip="127.0.0.1", port=3000)
        start_aut_output = StartApplicationUnderTestOutput.StartApplicationUnderTestOutput()
        start_aut_use_case.execute(start_aut_input, start_aut_output)

        aut_entity: ApplicationUnderTestEntity = self._aut_repository.find_by_id(
            start_aut_output.get_id())
        aut: ApplicationUnderTest = ApplicationUnderTestMapper.mapping_application_under_test_from(
            aut_entity)
        self.assertEqual(aut.get_id(), start_aut_output.get_id())
        server_response = requests.get(start_aut_output.get_url())
        self.assertEqual(200, server_response.status_code)

    def _execute_use_case_and_wait(self, applicationName: str):
        start_aut_use_case = StartApplicationUnderTestUserCase.StartApplicationUnderTestUserCase(
            repository=self._aut_repository, applicationHandler=self._application_handler)
        start_aut_input = StartApplicationUnderTestInput.StartApplicationUnderTestInput(
            applicationName=applicationName, ip="127.0.0.1", port=3001)
        start_aut_output = StartApplicationUnderTestOutput.StartApplicationUnderTestOutput()

        start_aut_use_case.execute(start_aut_input, start_aut_output)

        aut_entity: ApplicationUnderTestEntity = self._aut_repository.find_by_id(
            start_aut_output.get_id())
        aut: ApplicationUnderTest = ApplicationUnderTestMapper.mapping_application_under_test_from(
            aut_entity)
        self.assertEqual(aut.get_id(), start_aut_output.get_id())
        server_response = requests.get(start_aut_output.get_url())
        self.assertEqual(200, server_response.status_code)
