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
        self._inputTypeList: list = inputSpace.inputTypes
        self._inputCosineSimilarityThreshold: float = 0.3
        self._inputRewardCoefficient: float = 10.0
        self._cosineSimilarityText: str = ''

    def calculate_reward(self, episodeHandler: IEpisodeHandler):
        previousState: State = episodeHandler.get_all_state()[-2]

        if previousState.get_interacted_element() is None:
            self._logger.info('Interacted element is none, reward: 0')
            return 0

        if previousState.get_action_type() == "input":
            self._logger.info('Calculating input reward...')
            return self._get_input_value_reward(previousState=previousState)

        return 0

    def _get_input_value_reward(self, previousState: State):
        elementLabel = previousState.get_original_observation()["labelName"]

        if not elementLabel:
            self._logger.info("Label is empty")
            return 0.0

        inputCategory = self._inputTypeList[previousState.get_action_number()]

        categoryListTokens = inputSpace.CategoryListSingleton.get_instance().get_category_extend_list()[
            inputCategory]
        categoryListTokens.append(inputCategory)

        # vectorization whole String
        categoryListVector = FastTextSingleton.get_instance().get_words_vector(categoryListTokens)
        elementLabelVector = FastTextSingleton.get_instance().get_word_vector(word=elementLabel)

        labelCosineSimilarity = -1
        if categoryListVector:
            for categoryVector in categoryListVector:
                labelCosineSimilarity = max(
                    CosineSimilarityService.get_cosine_similarity(
                        categoryVector, elementLabelVector),
                    labelCosineSimilarity)

        if np.isnan(labelCosineSimilarity):
            reward = 0.0
            self._cosineSimilarityText = ''
            self._logger.info("label = NaN... ")
        else:
            self._cosineSimilarityText = elementLabel

            if labelCosineSimilarity < self._inputCosineSimilarityThreshold:
                self._logger.info("Cosine similarity lower than threshold.")
                self._cosineSimilarityText = ''

            reward = self._inputRewardCoefficient * labelCosineSimilarity

        reward = reward
        self._logger.info(f'Input reward: {reward}')
        return reward

    def get_cosine_similarity_text(self) -> str:
        return self._cosineSimilarityText
