class ExecuteActionOutput:
    def __init__(self):
        self._observation:[int] = []
        self._originalObservation = {}
        self._codeCoverageDict = {}
        self._reward = 0
        self._isDone = False
        self._previousState = None
        self._cosineSimilarityText: str = ''

    def setObservation(self, observation):
        self._observation = observation

    def getObservation(self):
        return self._observation

    def setOriginalObservation(self, originalObservation):
        self._originalObservation = originalObservation

    def getOriginalObservation(self):
        return self._originalObservation

    def setCodeCoverageDict(self, codeCoverageDict):
        self._codeCoverageDict = codeCoverageDict

    def getCodeCoverageDict(self):
        return self._codeCoverageDict

    def setReward(self, reward):
        self._reward = reward

    def getReward(self):
        return self._reward

    def setIsDone(self, isDone: bool):
        self._isDone = isDone

    def getIsDone(self):
        return self._isDone

    def setCosineSimilarityText(self, text: str):
        self._cosineSimilarityText = text

    def getCosineSimilarityText(self) -> str:
        return self._cosineSimilarityText
