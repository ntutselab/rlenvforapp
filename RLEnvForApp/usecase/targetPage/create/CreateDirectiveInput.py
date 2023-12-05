class CreateDirectiveInput:
    def __init__(self, targetPageId: str, episodeHandlerId: str):
        self._targetPageId = targetPageId
        self._episodeHandlerId = episodeHandlerId

    def getTargetPageId(self):
        return self._targetPageId

    def getEpisodeHandlerId(self):
        return self._episodeHandlerId