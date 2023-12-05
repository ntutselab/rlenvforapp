class StopApplicationUnderTestOutput:
    def __init__(self):
        self._url = ""

    def setUrl(self, url):
        self._url = url

    def getUrl(self):
        return self._url