class CreateDirectiveInput:
    def __init__(self, targetPageId: str, episodeHandlerId: str):
        self._targetPageId = targetPageId
        self._episodeHandlerId = episodeHandlerId

    def get_target_page_id(self):
        return self._targetPageId

    def get_episode_handler_id(self):
        return self._episodeHandlerId
