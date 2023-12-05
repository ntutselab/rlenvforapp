class ResetEnvironmentInput:
    def __init__(self, episodeIndex: int):
        self._episodeIndex = episodeIndex

    def getEpisodeIndex(self):
        return self._episodeIndex
