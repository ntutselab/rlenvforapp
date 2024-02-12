class ApplicationUnderTest:
    def __init__(self, id: str, applicationName: str, ip: str, port: int):
        self._id = id
        self._applicationName = applicationName
        self._ip = ip
        self._port = port

    def get_id(self):
        return self._id

    def get_application_name(self):
        return self._applicationName

    def get_ip(self):
        return self._ip

    def get_port(self):
        return self._port
