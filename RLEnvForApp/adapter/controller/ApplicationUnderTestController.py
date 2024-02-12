from RLEnvForApp.usecase.applicationUnderTest.start import (
    StartApplicationUnderTestInput, StartApplicationUnderTestOutput,
    StartApplicationUnderTestUserCase)
from RLEnvForApp.usecase.applicationUnderTest.stop import (
    StopApplicationUnderTestInput, StopApplicationUnderTestOutput,
    StopApplicationUnderTestUseCase)


class ApplicationUnderTestController:
    def __init__(self, applicationName: str, serverIP: str, port: int):
        self._autID = ""
        self._applicationName = applicationName
        self._serverIP = serverIP
        self._port = port
        self._isCacheModel = False

    def startAUTServer(self):
        startAUTUseCase = StartApplicationUnderTestUserCase.StartApplicationUnderTestUserCase()
        startAUTInput = StartApplicationUnderTestInput.StartApplicationUnderTestInput(
            applicationName=self._applicationName, ip=self._serverIP, port=self._port)
        startAUTOutput = StartApplicationUnderTestOutput.StartApplicationUnderTestOutput()
        startAUTUseCase.execute(startAUTInput, startAUTOutput)

        self._autID = startAUTOutput.getId()

    def stopAUTServer(self):
        stopAUTUseCase = StopApplicationUnderTestUseCase.StopApplicationUnderTestUseCase()
        stopAUTInput = StopApplicationUnderTestInput.StopApplicationUnderTestInput(
            id=self._autID)
        stopAUTOutput = StopApplicationUnderTestOutput.StopApplicationUnderTestOutput()
        stopAUTUseCase.execute(stopAUTInput, stopAUTOutput)

        self._autID = ""

    def resetAUTServer(self, isLegalDirective: bool):
        if self._autID != "" and isLegalDirective:
            self.stopAUTServer()
        # if not self._isCacheModel:
            self.startAUTServer()

    def setIsCacheModel(self, isCacheModel: bool):
        self._isCacheModel = isCacheModel
