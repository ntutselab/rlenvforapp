class CreateEpisodeHandlerInput:
    def __init__(self, episodeIndex: int):
        self._episode_index = episodeIndex

    def get_episode_index(self) -> int:
        return self._episode_index
