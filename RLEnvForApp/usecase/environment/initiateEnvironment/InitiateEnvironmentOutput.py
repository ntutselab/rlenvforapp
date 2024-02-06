class InitiateEnvironmentOutput:
    def __init__(self):
        self._observationSize = 0
        self._actionSpaceSize = 0
        self._actionList = []

    def setObservationSize(self, size):
        self._observationSize = size

    def getObservationSize(self):
        return self._observationSize

    def setActionSpaceSize(self, size: int):
        self._actionSpaceSize = size

    def getActionSpaceSize(self):
        return self._actionSpaceSize

    def setActionList(self, actionList):
        self._actionList = actionList

    def getActionList(self) -> [str]:
        return self._actionList
