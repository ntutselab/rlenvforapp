from dependency_injector.wiring import Provide, inject

from configuration.di.EnvironmentDIContainers import EnvironmentDIContainers
from RLEnvForApp.usecase.repository.ApplicationUnderTestRepository import \
    ApplicationUnderTestRepository

from ..applicationHandler.ApplicationHandler import ApplicationHandler
from ..mapper import ApplicationUnderTestMapper
from . import StopApplicationUnderTestInput, StopApplicationUnderTestOutput


class StopApplicationUnderTestUseCase:
    @inject
    def __init__(self, repository: ApplicationUnderTestRepository = Provide[EnvironmentDIContainers.applicationUnderTestRepository],
                 applicationHandler: ApplicationHandler = Provide[EnvironmentDIContainers.applicationHandler]):
        self._repository = repository
        self._applicationHandler = applicationHandler

    def execute(self, input: StopApplicationUnderTestInput.StopApplicationUnderTestInput,
                output: StopApplicationUnderTestOutput.StopApplicationUnderTestOutput):
        autId = input.get_id()
        autEntity = self._repository.find_by_id(autId)
        self._repository.delet_by_id(autId)
        aut = ApplicationUnderTestMapper.mapping_application_under_test_from(
            autEntity)
        autUrl = f"http://{aut.getIP()}:{str(aut.getPort())}"
        self._applicationHandler.stop(
            applicationName=aut.get_application_name(),
            ip=aut.get_ip(),
            port=aut.get_port())

        output.set_url(autUrl)
