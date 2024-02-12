class StopApplicationUnderTestOutput:
    def __init__(self):
        self._url = ""

    def set_url(self, url):
        self._url = url

    def get_url(self):
        return self._url
