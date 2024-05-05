class ExecuteActionInput:
    def __init__(self, actionNumber: int, episodeHandlerId: str, aut_name: str, url: str, xpath: str):
        self._actionNumber = actionNumber
        self._episodeHandlerId = episodeHandlerId
        self._aut_name = aut_name
        self._url = url
        self._xpath = xpath

    def getActionNumber(self):
        return self._actionNumber

    def getEpisodeHandlerId(self):
        return self._episodeHandlerId

    def getAutName(self):
        return self._aut_name

    def getUrl(self):
        return self._url

    def getXpath(self):
        return self._xpath