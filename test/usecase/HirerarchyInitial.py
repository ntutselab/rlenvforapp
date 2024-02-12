from RLEnvForApp.usecase.applicationUnderTest.applicationHandler.ApplicationHandler import ApplicationHandler
from RLEnvForApp.usecase.repository.ApplicationUnderTestRepository import ApplicationUnderTestRepository
from RLEnvForApp.usecase.applicationUnderTest.start import StartApplicationUnderTestUserCase, StartApplicationUnderTestInput, StartApplicationUnderTestOutput
from RLEnvForApp.usecase.applicationUnderTest.stop import StopApplicationUnderTestUseCase, StopApplicationUnderTestInput, StopApplicationUnderTestOutput


class HirerarchyInitial:
    def __init__(self, autRepository: ApplicationUnderTestRepository, applicationHandler: ApplicationHandler):
        self._autRepository = autRepository
        self._applicationHandler = applicationHandler

    def startAUTServer(self, applicationName):
        startAUTUseCase = StartApplicationUnderTestUserCase.StartApplicationUnderTestUserCase(repository=self._autRepository , applicationHandler=self._applicationHandler)
        startAUTInput = StartApplicationUnderTestInput.StartApplicationUnderTestInput(applicationName=applicationName, ip="127.0.0.1", port=3000)
        startAUTOutput = StartApplicationUnderTestOutput.StartApplicationUnderTestOutput()
        startAUTUseCase.execute(startAUTInput, startAUTOutput)

    def stopAUTServer(self, id):
        stopAUTUseCase = StopApplicationUnderTestUseCase.StopApplicationUnderTestUseCase(repository=self._autRepository, applicationHandler=self._applicationHandler)
        stopAUTInput = StopApplicationUnderTestInput.StopApplicationUnderTestInput(id=id)
        stopAUTOutput = StopApplicationUnderTestOutput.StopApplicationUnderTestOutput()
        stopAUTUseCase.execute(stopAUTInput, stopAUTOutput)
