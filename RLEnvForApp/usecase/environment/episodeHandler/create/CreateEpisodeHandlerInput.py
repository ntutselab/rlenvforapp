class CreateEpisodeHandlerInput:
    def __init__(self, episodeIndex: int):
        self._episodeIndex = episodeIndex

    def getEpisodeIndex(self) -> int:
        return self._episodeIndex
