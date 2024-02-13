class CreateDirectiveInput:
    def __init__(self, target_page_id: str, episode_handler_id: str):
        self._target_page_id = target_page_id
        self._episode_handler_id = episode_handler_id

    def get_target_page_id(self):
        return self._target_page_id

    def get_episode_handler_id(self):
        return self._episode_handler_id
