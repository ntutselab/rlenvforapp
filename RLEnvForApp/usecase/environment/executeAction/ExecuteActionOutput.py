class ExecuteActionOutput:
    def __init__(self):
        self._observation: [int] = []
        self._originalObservation = {}
        self._codeCoverageDict = {}
        self._reward = 0
        self._isDone = False
        self._previousState = None
        self._cosineSimilarityText: str = ''

    def set_observation(self, observation):
        self._observation = observation

    def get_observation(self):
        return self._observation

    def set_original_observation(self, originalObservation):
        self._originalObservation = originalObservation

    def get_original_observation(self):
        return self._originalObservation

    def set_code_coverage_dict(self, codeCoverageDict):
        self._codeCoverageDict = codeCoverageDict

    def get_code_coverage_dict(self):
        return self._codeCoverageDict

    def set_reward(self, reward):
        self._reward = reward

    def get_reward(self):
        return self._reward

    def set_is_done(self, isDone: bool):
        self._isDone = isDone

    def get_is_done(self):
        return self._isDone

    def set_cosine_similarity_text(self, text: str):
        self._cosineSimilarityText = text

    def get_cosine_similarity_text(self) -> str:
        return self._cosineSimilarityText
