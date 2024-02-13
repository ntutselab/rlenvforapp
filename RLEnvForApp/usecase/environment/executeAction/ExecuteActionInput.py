class ExecuteActionInput:
    def __init__(self, actionNumber: int, episode_handler_id: str):
        self._action_number = actionNumber
        self._episode_handler_id = episode_handler_id

    def get_action_number(self):
        return self._action_number

    def get_episode_handler_id(self):
        return self._episode_handler_id
