
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
        self._step_reward_coefficient = 1
        self._episode_reward_coefficient = 1000
        self._target_indication_service: ITargetIndicationService = HTMLLogIndicationService()
        self._action_indication_service: IActionIndicationService = CheckHTMLLogActionIndicationService()

        self._reward_coefficient: float = 10.0

        self._click_reward_coefficient: float = self._reward_coefficient
        self._change_focus_reward_coefficient: float = self._reward_coefficient
        self._input_reward_coefficient: float = self._reward_coefficient

        self._input_cosine_similarity_threshold: float = 0.3
        self._input_reward_base_line: float = 0.0

        self._input_type_list: list = inputSpace.inputTypes
        self._input_value_list: list = inputSpace.inputValues  # for Register

        self._cosine_similarity_text: str = ''

    def calculate_reward(self, episode_handler: IEpisodeHandler):
        previous_state: State = episode_handler.get_all_state()[-2]

        if episode_handler.is_done() and self._target_indication_service.is_conform(
                state=previous_state):
            reward = self._episode_reward_coefficient * \
                (1 / self._get_episode_step_fraction(episode_handler=episode_handler))
            self._logger.info(f'Form submitted reward: {reward}')
            # self._updateCategoryList(previousState)
            return reward

        if previous_state.get_interacted_element() is None:
            self._logger.info('Interacted element is none, reward: 0')
            return 0

        if self._action_indication_service.is_conform(state=previous_state):
            if previous_state.get_action_type() == "input":
                # self._updateCategoryList(previousState)
                return self._get_input_value_reward(previous_state=previous_state)

            if previous_state.get_action_type() == "click":
                return self._get_click_reward(previous_state=previous_state)

            self._logger.info('Action type is not input or click. reward: -10')
            return -10
        else:
            self._logger.info('Category not match record, reward: -10')
            return -10

    def _get_episode_step_fraction(self, episode_handler: IEpisodeHandler):
        episode_step_fraction = 0

        number_of_state = episode_handler.get_number_of_state()
        episode_step = episode_handler.get_episode_step()
        episode_step_fraction = (number_of_state - 1) / episode_step
        return episode_step_fraction

    def _get_input_value_reward(self, previous_state: State):
        element_label = previous_state.get_original_observation()["labelName"]

        if not element_label:
            self._logger.info("Label is empty")
            return 0.0

        input_category = self._input_type_list[previous_state.get_action_number()]

        category_list_tokens = list(
            map(CosineSimilarityService.getTokens, inputSpace.CategoryListSingleton.get_instance().get_category_extend_list()[input_category]))
        category_list_tokens.append(input_category)

        # vectorization whole String
        category_list_vector = list(
            map(FastTextSingleton.get_instance().getWordsVector, category_list_tokens))
        element_label_vector = FastTextSingleton.get_instance().get_word_vector(words=element_label)

        label_cosine_similarity = -1
        if category_list_vector:
            for categoryVector in category_list_vector:
                label_cosine_similarity = max(
                    CosineSimilarityService.get_cosine_similarity(
                        categoryVector, element_label_vector), label_cosine_similarity)

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

        reward = self._input_reward_base_line + reward
        self._logger.info(f'Input reward: {reward}')
        return reward

    def _get_click_reward(self, previous_state: State):
        tag = previous_state.get_interacted_element().get_tag_name()
        element_type = previous_state.get_interacted_element().get_type()
        if tag == "button" or (tag == 'input' and (
                element_type == 'submit' or element_type == 'image' or element_type == 'checkbox' or element_type == 'radio')):
            reward_revise = self._click_reward_coefficient * 1
        elif tag == "a":
            reward_revise = self._click_reward_coefficient * -0.5
        else:
            reward_revise = self._click_reward_coefficient * -0.3

        self._logger.info(f'Click tag: {tag}, type: {elementType}')
        self._logger.info(
            f'Click reward: {self._inputRewardBaseLine + rewardRevise}')
        return self._input_reward_base_line + reward_revise

    def _update_category_list(self, previous_state: State):
        category_extend_list = CategoryListSingleton.get_instance().get_category_extend_list()

        category = inputTypes[previous_state.get_action_number()]
        if self._cosine_similarity_text != '' and self._cosine_similarity_text not in category_extend_list[
                category]:
            category_extend_list[category].append(self._cosine_similarity_text)
            self._logger.info(
                f"Append [{self._cosineSimilarityText}] to category: {category}")

        CategoryListSingleton.get_instance().set_category_extend_list(category_extend_list)

    def get_cosine_similarity_text(self) -> str:
        return self._cosine_similarity_text
