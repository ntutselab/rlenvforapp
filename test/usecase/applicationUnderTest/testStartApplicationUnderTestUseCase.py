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
        self._autRepository = InMemoryApplicationUnderTestRepository()
        self._applicationHandler = DockerServerHandler(
            "RLEnvForApp/application/serverInstance")
        self._hirerarchyInitial = HirerarchyInitial(
            autRepository=self._autRepository,
            applicationHandler=self._applicationHandler)

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
        startAUTUseCase = StartApplicationUnderTestUserCase.StartApplicationUnderTestUserCase(
            repository=self._autRepository,
            applicationHandler=DockerServerHandler("RLEnvForApp/application/serverInstance"))
        startAUTInput = StartApplicationUnderTestInput.StartApplicationUnderTestInput(
            applicationName="timeoff_management_with_coverage", ip="127.0.0.1", port=3000)
        startAUTOutput = StartApplicationUnderTestOutput.StartApplicationUnderTestOutput()
        startAUTUseCase.execute(startAUTInput, startAUTOutput)

        autEntity: ApplicationUnderTestEntity = self._autRepository.find_by_id(
            startAUTOutput.get_id())
        aut: ApplicationUnderTest = ApplicationUnderTestMapper.mapping_application_under_test_from(
            autEntity)
        self.assertEqual(aut.get_id(), startAUTOutput.get_id())
        serverResponse = requests.get(startAUTOutput.get_url())
        self.assertEqual(200, serverResponse.status_code)

        startAUTUseCase = StartApplicationUnderTestUserCase.StartApplicationUnderTestUserCase(
            repository=self._autRepository,
            applicationHandler=DockerServerHandler("RLEnvForApp/application/serverInstance"))
        startAUTInput = StartApplicationUnderTestInput.StartApplicationUnderTestInput(
            applicationName="timeoff_management_with_coverage", ip="127.0.0.1", port=3000)
        startAUTOutput = StartApplicationUnderTestOutput.StartApplicationUnderTestOutput()
        startAUTUseCase.execute(startAUTInput, startAUTOutput)

        autEntity: ApplicationUnderTestEntity = self._autRepository.find_by_id(
            startAUTOutput.get_id())
        aut: ApplicationUnderTest = ApplicationUnderTestMapper.mapping_application_under_test_from(
            autEntity)
        self.assertEqual(aut.get_id(), startAUTOutput.get_id())
        serverResponse = requests.get(startAUTOutput.get_url())
        self.assertEqual(200, serverResponse.status_code)

        startAUTUseCase = StartApplicationUnderTestUserCase.StartApplicationUnderTestUserCase(
            repository=self._autRepository,
            applicationHandler=DockerServerHandler("RLEnvForApp/application/serverInstance"))
        startAUTInput = StartApplicationUnderTestInput.StartApplicationUnderTestInput(
            applicationName="nodebb_with_coverage", ip="127.0.0.1", port=3000)
        startAUTOutput = StartApplicationUnderTestOutput.StartApplicationUnderTestOutput()
        startAUTUseCase.execute(startAUTInput, startAUTOutput)

        autEntity: ApplicationUnderTestEntity = self._autRepository.find_by_id(
            startAUTOutput.get_id())
        aut: ApplicationUnderTest = ApplicationUnderTestMapper.mapping_application_under_test_from(
            autEntity)
        self.assertEqual(aut.get_id(), startAUTOutput.get_id())
        serverResponse = requests.get(startAUTOutput.get_url())
        self.assertEqual(200, serverResponse.status_code)

    def _execute_use_case_and_wait(self, applicationName: str):
        startAUTUseCase = StartApplicationUnderTestUserCase.StartApplicationUnderTestUserCase(
            repository=self._autRepository, applicationHandler=self._applicationHandler)
        startAUTInput = StartApplicationUnderTestInput.StartApplicationUnderTestInput(
            applicationName=applicationName, ip="127.0.0.1", port=3001)
        startAUTOutput = StartApplicationUnderTestOutput.StartApplicationUnderTestOutput()

        startAUTUseCase.execute(startAUTInput, startAUTOutput)

        autEntity: ApplicationUnderTestEntity = self._autRepository.find_by_id(
            startAUTOutput.get_id())
        aut: ApplicationUnderTest = ApplicationUnderTestMapper.mapping_application_under_test_from(
            autEntity)
        self.assertEqual(aut.get_id(), startAUTOutput.get_id())
        serverResponse = requests.get(startAUTOutput.get_url())
        self.assertEqual(200, serverResponse.status_code)
