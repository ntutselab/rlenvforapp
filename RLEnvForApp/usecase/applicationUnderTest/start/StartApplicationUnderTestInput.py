class StartApplicationUnderTestInput:
    def __init__(self, applicationName, ip, port):
        self._application_name = applicationName
        self._ip = ip
        self._port = port

    def get_application_name(self):
        return self._application_name

    def get_ip(self):
        return self._ip

    def get_port(self):
        return self._port
