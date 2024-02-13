class InitiateEnvironmentOutput:
    def __init__(self):
        self._observation_size = 0
        self._action_space_size = 0
        self._action_list = []

    def set_observation_size(self, size):
        self._observation_size = size

    def get_observation_size(self):
        return self._observation_size

    def set_action_space_size(self, size: int):
        self._action_space_size = size

    def get_action_space_size(self):
        return self._action_space_size

    def set_action_list(self, action_list):
        self._action_list = action_list

    def get_action_list(self) -> [str]:
        return self._action_list
