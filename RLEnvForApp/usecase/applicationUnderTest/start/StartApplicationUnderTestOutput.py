class StartApplicationUnderTestOutput:
    def __init__(self):
        self._url = ""
        self._id = ""

    def setId(self, id):
        self._id = id

    def getId(self):
        return self._id

    def setUrl(self, url):
        self._url = url

    def getUrl(self):
        return self._url
