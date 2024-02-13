import numpy as np

from RLEnvForApp.domain.environment import inputSpace
from RLEnvForApp.domain.environment.cosineSimilarityService.CosineSimilarityService import \
    CosineSimilarityService
from RLEnvForApp.domain.environment.episodeHandler.IEpisodeHandler import \
    IEpisodeHandler
from RLEnvForApp.domain.environment.observationService.converter.FastTextSingleton import \
    FastTextSingleton
from RLEnvForApp.domain.environment.rewardCalculatorService.IRewardCalculatorService import \
    IRewardCalculatorService
from RLEnvForApp.domain.environment.state.State import State
from RLEnvForApp.logger.logger import Logger


class VerifyPhaseRewardCalculatorService(IRewardCalculatorService):
    def __init__(self):
        super().__init__()
        self._logger = Logger()
        self._input_type_list: list = inputSpace.inputTypes
        self._input_cosine_similarity_threshold: float = 0.3
        self._input_reward_coefficient: float = 10.0
        self._cosine_similarity_text: str = ''

    def calculate_reward(self, episode_handler: IEpisodeHandler):
        previous_state: State = episode_handler.get_all_state()[-2]

        if previous_state.get_interacted_element() is None:
            self._logger.info('Interacted element is none, reward: 0')
            return 0

        if previous_state.get_action_type() == "input":
            self._logger.info('Calculating input reward...')
            return self._get_input_value_reward(previous_state=previous_state)

        return 0

    def _get_input_value_reward(self, previous_state: State):
        element_label = previous_state.get_original_observation()["labelName"]

        if not element_label:
            self._logger.info("Label is empty")
            return 0.0

        input_category = self._input_type_list[previous_state.get_action_number()]

        category_list_tokens = inputSpace.CategoryListSingleton.get_instance().get_category_extend_list()[
            input_category]
        category_list_tokens.append(input_category)

        # vectorization whole String
        category_list_vector = FastTextSingleton.get_instance().get_words_vector(category_list_tokens)
        element_label_vector = FastTextSingleton.get_instance().get_word_vector(word=element_label)

        label_cosine_similarity = -1
        if category_list_vector:
            for categoryVector in category_list_vector:
                label_cosine_similarity = max(
                    CosineSimilarityService.get_cosine_similarity(
                        categoryVector, element_label_vector),
                    label_cosine_similarity)

        if np.isnan(label_cosine_similarity):
            reward = 0.0
            self._cosine_similarity_text = ''
            self._logger.info("label = NaN... ")
        else:
            self._cosine_similarity_text = element_label

            if label_cosine_similarity < self._input_cosine_similarity_threshold:
                self._logger.info("Cosine similarity lower than threshold.")
                self._cosine_similarity_text = ''

            reward = self._input_reward_coefficient * label_cosine_similarity

        reward = reward
        self._logger.info(f'Input reward: {reward}')
        return reward

    def get_cosine_similarity_text(self) -> str:
        return self._cosine_similarity_text
