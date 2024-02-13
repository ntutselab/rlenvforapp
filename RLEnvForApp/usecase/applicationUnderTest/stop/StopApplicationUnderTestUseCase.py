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
        self._application_handler = applicationHandler

    def execute(self, input: StopApplicationUnderTestInput.StopApplicationUnderTestInput,
                output: StopApplicationUnderTestOutput.StopApplicationUnderTestOutput):
        aut_id = input.get_id()
        aut_entity = self._repository.find_by_id(aut_id)
        self._repository.delet_by_id(aut_id)
        aut = ApplicationUnderTestMapper.mapping_application_under_test_from(
            aut_entity)
        aut_url = f"http://{aut.getIP()}:{str(aut.getPort())}"
        self._application_handler.stop(
            applicationName=aut.get_application_name(),
            ip=aut.get_ip(),
            port=aut.get_port())

        output.set_url(aut_url)
