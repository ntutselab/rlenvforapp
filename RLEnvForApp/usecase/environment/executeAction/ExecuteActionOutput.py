class ExecuteActionOutput:
    def __init__(self):
        self._observation: [int] = []
        self._original_observation = {}
        self._code_coverage_dict = {}
        self._reward = 0
        self._is_done = False
        self._previous_state = None
        self._cosine_similarity_text: str = ''

    def set_observation(self, observation):
        self._observation = observation

    def get_observation(self):
        return self._observation

    def set_original_observation(self, originalObservation):
        self._original_observation = originalObservation

    def get_original_observation(self):
        return self._original_observation

    def set_code_coverage_dict(self, code_coverage_dict):
        self._code_coverage_dict = code_coverage_dict

    def get_code_coverage_dict(self):
        return self._code_coverage_dict

    def set_reward(self, reward):
        self._reward = reward

    def get_reward(self):
        return self._reward

    def set_is_done(self, is_done: bool):
        self._is_done = is_done

    def get_is_done(self):
        return self._is_done

    def set_cosine_similarity_text(self, text: str):
        self._cosine_similarity_text = text

    def get_cosine_similarity_text(self) -> str:
        return self._cosine_similarity_text
