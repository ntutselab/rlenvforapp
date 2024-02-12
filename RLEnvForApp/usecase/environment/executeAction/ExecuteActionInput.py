class ExecuteActionInput:
    def __init__(self, actionNumber: int, episodeHandlerId: str):
        self._actionNumber = actionNumber
        self._episodeHandlerId = episodeHandlerId

    def get_action_number(self):
        return self._actionNumber

    def get_episode_handler_id(self):
        return self._episodeHandlerId
