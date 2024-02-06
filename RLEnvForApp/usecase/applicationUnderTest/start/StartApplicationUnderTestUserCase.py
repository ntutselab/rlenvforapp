from RLEnvForApp.domain.applicationUnderTest.ApplicationUnderTest import ApplicationUnderTest
from . import (StartApplicationUnderTestInput, StartApplicationUnderTestOutput)
import uuid

from RLEnvForApp.usecase.repository.ApplicationUnderTestRepository import ApplicationUnderTestRepository
from ..applicationHandler.ApplicationHandler import ApplicationHandler
from ..mapper import ApplicationUnderTestMapper

from configuration.di.EnvironmentDIContainers import EnvironmentDIContainers
from dependency_injector.wiring import inject, Provide


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
            applicationName=input.getApplicationName(),
            ip=input.getIP(),
            port=input.getPort())
        self._repository.add(
            ApplicationUnderTestMapper.mappingApplicationUnderTestEntityFrom(
                aut=aut))
        self._applicationHandler.start(
            applicationName=aut.getApplicationName(),
            ip=aut.getIP(),
            port=aut.getPort())

        output.setUrl("http://{ip}:{port}".format(ip=aut.getIP(), port=str(aut.getPort())))
        output.setId(aut.getId())
