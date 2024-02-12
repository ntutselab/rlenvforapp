class InitiateEnvironmentOutput:
    def __init__(self):
        self._observationSize = 0
        self._actionSpaceSize = 0
        self._actionList = []

    def set_observation_size(self, size):
        self._observationSize = size

    def get_observation_size(self):
        return self._observationSize

    def set_action_space_size(self, size: int):
        self._actionSpaceSize = size

    def get_action_space_size(self):
        return self._actionSpaceSize

    def set_action_list(self, actionList):
        self._actionList = actionList

    def get_action_list(self) -> [str]:
        return self._actionList
