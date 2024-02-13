from RLEnvForApp.usecase.applicationUnderTest.start import (
    StartApplicationUnderTestInput, StartApplicationUnderTestOutput,
    StartApplicationUnderTestUserCase)
from RLEnvForApp.usecase.applicationUnderTest.stop import (
    StopApplicationUnderTestInput, StopApplicationUnderTestOutput,
    StopApplicationUnderTestUseCase)


class ApplicationUnderTestController:
    def __init__(self, applicationName: str, serverIP: str, port: int):
        self._aut_id = ""
        self._application_name = applicationName
        self._server_ip = serverIP
        self._port = port
        self._is_cache_model = False

    def start_aut_server(self):
        start_aut_use_case = StartApplicationUnderTestUserCase.StartApplicationUnderTestUserCase()
        start_aut_input = StartApplicationUnderTestInput.StartApplicationUnderTestInput(
            applicationName=self._application_name, ip=self._server_ip, port=self._port)
        start_aut_output = StartApplicationUnderTestOutput.StartApplicationUnderTestOutput()
        start_aut_use_case.execute(start_aut_input, start_aut_output)

        self._aut_id = start_aut_output.get_id()

    def stop_aut_server(self):
        stop_aut_use_case = StopApplicationUnderTestUseCase.StopApplicationUnderTestUseCase()
        stop_aut_input = StopApplicationUnderTestInput.StopApplicationUnderTestInput(
            id=self._aut_id)
        stop_aut_output = StopApplicationUnderTestOutput.StopApplicationUnderTestOutput()
        stop_aut_use_case.execute(stop_aut_input, stop_aut_output)

        self._aut_id = ""

    def reset_aut_server(self, is_legal_directive: bool):
        if self._aut_id != "" and is_legal_directive:
            self.stop_aut_server()
        # if not self._isCacheModel:
            self.start_aut_server()

    def set_is_cache_model(self, isCacheModel: bool):
        self._is_cache_model = isCacheModel
