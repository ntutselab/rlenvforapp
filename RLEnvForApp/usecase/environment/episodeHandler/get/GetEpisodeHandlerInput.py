class GetEpisodeHandlerInput:
    def __init__(self, episodeHandlerId: str):
        self._episodeHandlerId = episodeHandlerId

    def get_episode_handler_id(self) -> str:
        return self._episodeHandlerId
