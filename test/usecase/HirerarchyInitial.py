from RLEnvForApp.usecase.applicationUnderTest.applicationHandler.ApplicationHandler import \
    ApplicationHandler
from RLEnvForApp.usecase.applicationUnderTest.start import (
    StartApplicationUnderTestInput, StartApplicationUnderTestOutput,
    StartApplicationUnderTestUserCase)
from RLEnvForApp.usecase.applicationUnderTest.stop import (
    StopApplicationUnderTestInput, StopApplicationUnderTestOutput,
    StopApplicationUnderTestUseCase)
from RLEnvForApp.usecase.repository.ApplicationUnderTestRepository import \
    ApplicationUnderTestRepository


class HirerarchyInitial:
    def __init__(self, autRepository: ApplicationUnderTestRepository,
                 applicationHandler: ApplicationHandler):
        self._aut_repository = autRepository
        self._application_handler = applicationHandler

    def start_aut_server(self, applicationName):
        start_aut_use_case = StartApplicationUnderTestUserCase.StartApplicationUnderTestUserCase(
            repository=self._aut_repository, applicationHandler=self._application_handler)
        start_aut_input = StartApplicationUnderTestInput.StartApplicationUnderTestInput(
            applicationName=applicationName, ip="127.0.0.1", port=3000)
        start_aut_output = StartApplicationUnderTestOutput.StartApplicationUnderTestOutput()
        start_aut_use_case.execute(start_aut_input, start_aut_output)

    def stop_aut_server(self, id):
        stop_aut_use_case = StopApplicationUnderTestUseCase.StopApplicationUnderTestUseCase(
            repository=self._aut_repository, applicationHandler=self._application_handler)
        stop_aut_input = StopApplicationUnderTestInput.StopApplicationUnderTestInput(
            id=id)
        stop_aut_output = StopApplicationUnderTestOutput.StopApplicationUnderTestOutput()
        stop_aut_use_case.execute(stop_aut_input, stop_aut_output)
