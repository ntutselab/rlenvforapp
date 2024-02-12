class StartApplicationUnderTestOutput:
    def __init__(self):
        self._url = ""
        self._id = ""

    def set_id(self, id):
        self._id = id

    def get_id(self):
        return self._id

    def set_url(self, url):
        self._url = url

    def get_url(self):
        return self._url
