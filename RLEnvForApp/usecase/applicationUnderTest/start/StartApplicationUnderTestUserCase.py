import uuid

from dependency_injector.wiring import Provide, inject

from configuration.di.EnvironmentDIContainers import EnvironmentDIContainers
from RLEnvForApp.domain.applicationUnderTest.ApplicationUnderTest import \
    ApplicationUnderTest
from RLEnvForApp.usecase.repository.ApplicationUnderTestRepository import \
    ApplicationUnderTestRepository

from ..applicationHandler.ApplicationHandler import ApplicationHandler
from ..mapper import ApplicationUnderTestMapper
from . import StartApplicationUnderTestInput, StartApplicationUnderTestOutput


class StartApplicationUnderTestUserCase:
    @inject
    def __init__(self, repository: ApplicationUnderTestRepository = Provide[EnvironmentDIContainers.applicationUnderTestRepository],
                 applicationHandler: ApplicationHandler = Provide[EnvironmentDIContainers.applicationHandler]):
        self._repository = repository
        self._applicationHandler = applicationHandler

    def execute(self, input: StartApplicationUnderTestInput.StartApplicationUnderTestInput,
                output: StartApplicationUnderTestOutput.StartApplicationUnderTestOutput):
        aut = ApplicationUnderTest(
            id=str(
                uuid.uuid4()),
            applicationName=input.get_application_name(),
            ip=input.get_ip(),
            port=input.get_port())
        self._repository.add(
            ApplicationUnderTestMapper.mapping_application_under_test_entity_from(
                aut=aut))
        self._applicationHandler.start(
            applicationName=aut.get_application_name(),
            ip=aut.get_ip(),
            port=aut.get_port())

        output.set_url(
            f"http://{aut.getIP()}:{str(aut.getPort())}")
        output.set_id(aut.get_id())
