class StartApplicationUnderTestInput:
    def __init__(self, applicationName, ip, port):
        self._applicationName = applicationName
        self._ip = ip
        self._port = port

    def getApplicationName(self):
        return self._applicationName

    def getIP(self):
        return self._ip

    def getPort(self):
        return self._port
