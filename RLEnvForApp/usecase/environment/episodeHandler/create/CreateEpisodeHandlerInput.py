class CreateEpisodeHandlerInput:
    def __init__(self, episodeIndex: int):
        self._episodeIndex = episodeIndex

    def get_episode_index(self) -> int:
        return self._episodeIndex
