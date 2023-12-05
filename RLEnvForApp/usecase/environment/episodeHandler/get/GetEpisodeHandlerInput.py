class GetEpisodeHandlerInput:
    def __init__(self, episodeHandlerId: str):
        self._episodeHandlerId = episodeHandlerId

    def getEpisodeHandlerId(self) -> str:
        return self._episodeHandlerId