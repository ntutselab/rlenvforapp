
import numpy as np

from RLEnvForApp.domain.environment import inputSpace
from RLEnvForApp.domain.environment.cosineSimilarityService.CosineSimilarityService import \
    CosineSimilarityService
from RLEnvForApp.domain.environment.episodeHandler.IEpisodeHandler import \
    IEpisodeHandler
from RLEnvForApp.domain.environment.inputSpace import (CategoryListSingleton,
                                                       inputTypes)
from RLEnvForApp.domain.environment.observationService.converter.FastTextSingleton import \
    FastTextSingleton
from RLEnvForApp.domain.environment.rewardCalculatorService.ActionIndicationService.IActionIndicationService import \
    IActionIndicationService
from RLEnvForApp.domain.environment.rewardCalculatorService.IRewardCalculatorService import \
    IRewardCalculatorService
from RLEnvForApp.domain.environment.state.State import State
from RLEnvForApp.domain.targetPage.TargetIndicationService.ITargetIndicationService import \
    ITargetIndicationService
from RLEnvForApp.logger.logger import Logger
from RLEnvForApp.usecase.environment.executeAction.ActionIndicationService.CheckHTMLLogActionIndicationService import \
    CheckHTMLLogActionIndicationService
from RLEnvForApp.usecase.targetPage.ITargetIndicationService.HTMLLogIndicationService import \
    HTMLLogIndicationService


class CosineSimilarityRewardCalculatorService(IRewardCalculatorService):
    def __init__(self):
        super().__init__()
        self._logger = Logger()
        self._stepRewardCoefficient = 1
        self._episodeRewardCoefficient = 1000
        self._targetIndicationService: ITargetIndicationService = HTMLLogIndicationService()
        self._actionIndicationService: IActionIndicationService = CheckHTMLLogActionIndicationService()

        self._rewardCoefficient: float = 10.0

        self._clickRewardCoefficient: float = self._rewardCoefficient
        self._changeFocusRewardCoefficient: float = self._rewardCoefficient
        self._inputRewardCoefficient: float = self._rewardCoefficient

        self._inputCosineSimilarityThreshold: float = 0.3
        self._inputRewardBaseLine: float = 0.0

        self._inputTypeList: list = inputSpace.inputTypes
        self._inputValueList: list = inputSpace.inputValues  # for Register

        self._cosineSimilarityText: str = ''

    def calculate_reward(self, episodeHandler: IEpisodeHandler):
        previousState: State = episodeHandler.get_all_state()[-2]

        if episodeHandler.is_done() and self._targetIndicationService.is_conform(
                state=previousState):
            reward = self._episodeRewardCoefficient * \
                (1 / self._get_episode_step_fraction(episodeHandler=episodeHandler))
            self._logger.info(f'Form submitted reward: {reward}')
            # self._updateCategoryList(previousState)
            return reward

        if previousState.get_interacted_element() is None:
            self._logger.info('Interacted element is none, reward: 0')
            return 0

        if self._actionIndicationService.is_conform(state=previousState):
            if previousState.get_action_type() == "input":
                # self._updateCategoryList(previousState)
                return self._get_input_value_reward(previousState=previousState)

            if previousState.get_action_type() == "click":
                return self._get_click_reward(previousState=previousState)

            self._logger.info('Action type is not input or click. reward: -10')
            return -10
        else:
            self._logger.info('Category not match record, reward: -10')
            return -10

    def _get_episode_step_fraction(self, episodeHandler: IEpisodeHandler):
        episodeStepFraction = 0

        numberOfState = episodeHandler.get_number_of_state()
        episodeStep = episodeHandler.get_episode_step()
        episodeStepFraction = (numberOfState - 1) / episodeStep
        return episodeStepFraction

    def _get_input_value_reward(self, previousState: State):
        elementLabel = previousState.get_original_observation()["labelName"]

        if not elementLabel:
            self._logger.info("Label is empty")
            return 0.0

        inputCategory = self._inputTypeList[previousState.get_action_number()]

        categoryListTokens = list(
            map(CosineSimilarityService.getTokens, inputSpace.CategoryListSingleton.get_instance().get_category_extend_list()[inputCategory]))
        categoryListTokens.append(inputCategory)

        # vectorization whole String
        categoryListVector = list(
            map(FastTextSingleton.get_instance().getWordsVector, categoryListTokens))
        elementLabelVector = FastTextSingleton.get_instance().get_word_vector(words=elementLabel)

        labelCosineSimilarity = -1
        if categoryListVector:
            for categoryVector in categoryListVector:
                labelCosineSimilarity = max(
                    CosineSimilarityService.get_cosine_similarity(
                        categoryVector, elementLabelVector), labelCosineSimilarity)

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

        reward = self._inputRewardBaseLine + reward
        self._logger.info(f'Input reward: {reward}')
        return reward

    def _get_click_reward(self, previousState: State):
        tag = previousState.get_interacted_element().get_tag_name()
        elementType = previousState.get_interacted_element().get_type()
        if tag == "button" or (tag == 'input' and (
                elementType == 'submit' or elementType == 'image' or elementType == 'checkbox' or elementType == 'radio')):
            rewardRevise = self._clickRewardCoefficient * 1
        elif tag == "a":
            rewardRevise = self._clickRewardCoefficient * -0.5
        else:
            rewardRevise = self._clickRewardCoefficient * -0.3

        self._logger.info(f'Click tag: {tag}, type: {elementType}')
        self._logger.info(
            f'Click reward: {self._inputRewardBaseLine + rewardRevise}')
        return self._inputRewardBaseLine + rewardRevise

    def _update_category_list(self, previousState: State):
        categoryExtendList = CategoryListSingleton.get_instance().get_category_extend_list()

        category = inputTypes[previousState.get_action_number()]
        if self._cosineSimilarityText != '' and self._cosineSimilarityText not in categoryExtendList[
                category]:
            categoryExtendList[category].append(self._cosineSimilarityText)
            self._logger.info(
                f"Append [{self._cosineSimilarityText}] to category: {category}")

        CategoryListSingleton.get_instance().set_category_extend_list(categoryExtendList)

    def get_cosine_similarity_text(self) -> str:
        return self._cosineSimilarityText
