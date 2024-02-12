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
        self._autRepository = autRepository
        self._applicationHandler = applicationHandler

    def start_aut_server(self, applicationName):
        startAUTUseCase = StartApplicationUnderTestUserCase.StartApplicationUnderTestUserCase(
            repository=self._autRepository, applicationHandler=self._applicationHandler)
        startAUTInput = StartApplicationUnderTestInput.StartApplicationUnderTestInput(
            applicationName=applicationName, ip="127.0.0.1", port=3000)
        startAUTOutput = StartApplicationUnderTestOutput.StartApplicationUnderTestOutput()
        startAUTUseCase.execute(startAUTInput, startAUTOutput)

    def stop_aut_server(self, id):
        stopAUTUseCase = StopApplicationUnderTestUseCase.StopApplicationUnderTestUseCase(
            repository=self._autRepository, applicationHandler=self._applicationHandler)
        stopAUTInput = StopApplicationUnderTestInput.StopApplicationUnderTestInput(
            id=id)
        stopAUTOutput = StopApplicationUnderTestOutput.StopApplicationUnderTestOutput()
        stopAUTUseCase.execute(stopAUTInput, stopAUTOutput)
