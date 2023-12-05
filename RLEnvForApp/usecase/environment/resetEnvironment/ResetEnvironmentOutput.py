class ResetEnvironmentOutput:
    def __init__(self):
        self._observation: [int] = []
        self._episodeHandlerId = ""
        self._targetPageUrl = ""
        self._targetPageId = ""
        self._formXPath = ""
        self._originalObservation = {}

    def setObservation(self, observation):
        self._observation = observation

    def getObservation(self):
        return self._observation

    def setOriginalObservation(self, originalObservation: dict):
        self._originalObservation = originalObservation

    def getOriginalObservation(self):
        return self._originalObservation

    def setTargetPageUrl(self, url: str):
        self._targetPageUrl = url

    def getTargetPageUrl(self):
        return self._targetPageUrl

    def setTargetPageId(self, id: str):
        self._targetPageId = id

    def getTargetPageId(self):
        return self._targetPageId

    def getFormXPath(self):
        return self._formXPath

    def setFormXPath(self, formXPath: str):
        self._formXPath = formXPath

    def setEpisodeHandlerId(self, id: str):
        self._episodeHandlerId = id

    def getEpisodeHandlerId(self):
        return self._episodeHandlerId
