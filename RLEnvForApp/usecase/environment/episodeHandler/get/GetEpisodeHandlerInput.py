class GetEpisodeHandlerInput:
    def __init__(self, episode_handler_id: str):
        self._episode_handler_id = episode_handler_id

    def get_episode_handler_id(self) -> str:
        return self._episode_handler_id
