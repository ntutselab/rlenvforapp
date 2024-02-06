from . import (StopApplicationUnderTestInput, StopApplicationUnderTestOutput)
from ..applicationHandler.ApplicationHandler import ApplicationHandler
from ..mapper import ApplicationUnderTestMapper
from RLEnvForApp.usecase.repository.ApplicationUnderTestRepository import ApplicationUnderTestRepository

from configuration.di.EnvironmentDIContainers import EnvironmentDIContainers
from dependency_injector.wiring import inject, Provide


class StopApplicationUnderTestUseCase:
    @inject
    def __init__(self, repository: ApplicationUnderTestRepository = Provide[EnvironmentDIContainers.applicationUnderTestRepository],
                 applicationHandler: ApplicationHandler = Provide[EnvironmentDIContainers.applicationHandler]):
        self._repository = repository
        self._applicationHandler = applicationHandler

    def execute(self, input: StopApplicationUnderTestInput.StopApplicationUnderTestInput,
                output: StopApplicationUnderTestOutput.StopApplicationUnderTestOutput):
        autId = input.getId()
        autEntity = self._repository.findById(autId)
        self._repository.deletById(autId)
        aut = ApplicationUnderTestMapper.mappingApplicationUnderTestFrom(autEntity)
        autUrl = "http://{ip}:{port}".format(ip=aut.getIP(), port=str(aut.getPort()))
        self._applicationHandler.stop(
            applicationName=aut.getApplicationName(),
            ip=aut.getIP(),
            port=aut.getPort())

        output.setUrl(autUrl)
