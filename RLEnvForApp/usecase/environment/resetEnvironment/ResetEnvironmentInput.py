class ResetEnvironmentInput:
    def __init__(self, episodeIndex: int):
        self._episodeIndex = episodeIndex

    def get_episode_index(self):
        return self._episodeIndex
