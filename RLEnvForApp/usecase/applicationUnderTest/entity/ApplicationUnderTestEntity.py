class ApplicationUnderTestEntity:
    def __init__(self, id: str, applicationName: str, ip: str, port: int):
        self._id = id
        self._applicationName = applicationName
        self._ip = ip
        self._port = port

    def getId(self):
        return self._id

    def getapplicationName(self):
        return self._applicationName

    def getIP(self):
        return self._ip

    def getPort(self):
        return self._port
