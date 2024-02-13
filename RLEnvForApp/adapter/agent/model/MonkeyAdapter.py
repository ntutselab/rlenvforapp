import random

import numpy as np

from RLEnvForApp.domain.environment import inputSpace
from RLEnvForApp.domain.environment.cosineSimilarityService.CosineSimilarityService import \
    CosineSimilarityService
from RLEnvForApp.domain.environment.observationService.converter.FastTextSingleton import \
    FastTextSingleton
from RLEnvForApp.logger.logger import Logger


class MonkeyAdapter:
    def __init__(self, policy, env):
        self._env = env
        self._input_type_list: list = inputSpace.inputTypes
        self._input_type_list_length = len(inputSpace.inputTypes)

    def setup_model(self):
        pass

    def learn(self, total_timesteps, callback=None,
              log_interval=100, tb_log_name="run", reset_num_timesteps=True, replay_wrapper=None):

        observation = self._env.reset()
        for i in range(0, total_timesteps):
            action = self.predict(observation=observation)
            observation, rewards, is_done, info = self._env.step(action)

    def predict(self, observation, state=None, mask=None, deterministic=False):
        # return str(self._env.action_space.sample()), None  # random select
        return self.select_action_by_cosine_similarity(observation), None

    def action_probability(self, observation, state=None,
                           mask=None, actions=None, logp=False):
        pass

    def save(self, save_path, cloudpickle=False):
        pass

    @classmethod
    def load(cls, load_path, env=None, custom_objects=None, **kwargs):
        pass

    def select_action_by_cosine_similarity(self, observation):
        similarity = 0.0
        input_type_index = None

        aut_operator = self._env.env_method(method_name="getAUTOperator")[0]
        focused_app_element = aut_operator.get_focused_app_element()

        if not focused_app_element:
            return str(self._env.action_space.sample())

        tag_name = focused_app_element.get_tag_name()
        element_type = focused_app_element.get_type()
        if tag_name == "button" or tag_name == "a" or \
                (tag_name == 'input' and (
                    element_type == 'submit' or element_type == 'image' or element_type == 'checkbox' or element_type == 'radio')):
            similarity = 1.0
            input_type_index = 0
            for app_element in aut_operator.get_all_selected_app_elements():
                if app_element == focused_app_element:
                    continue
                if not app_element.get_value():
                    similarity = 0.0
                    input_type_index = None

        for i in range(0, self._input_type_list_length):
            category = self._input_type_list[i]

            category_list_tokens = inputSpace.CategoryListSingleton.get_instance().get_category_extend_list()[
                category]
            category_list_tokens.append(category)

            # vectorization whole String
            category_list_vector = FastTextSingleton.get_instance().get_words_vector(category_list_tokens)
            element_label_vector = np.array(observation[:, :300, :].reshape(300))

            label_cosine_similarity = -1
            if category_list_vector:
                for categoryVector in category_list_vector:
                    label_cosine_similarity = max(
                        CosineSimilarityService.get_cosine_similarity(categoryVector, element_label_vector), label_cosine_similarity)

            if np.isnan(label_cosine_similarity):
                continue
            else:
                if label_cosine_similarity > similarity:
                    similarity = label_cosine_similarity
                    input_type_index = i

        if input_type_index is None:
            return str(self._env.action_space.sample())

        action_list = list(range(self._input_type_list_length))
        probabilities = [1 / self._input_type_list_length for _ in action_list]
        probabilities[input_type_index] *= 30
        probabilities = [float(weight) / sum(action_list)
                         for weight in probabilities]
        random_action_type = random.choices(action_list, probabilities)[0]

        Logger().info(
            f"Similarity: {similarity}, Action: {self._inputTypeList[inputTypeIndex]}")
        Logger().info(f"Final action: {self._inputTypeList[randomActionType]}")

        return str(random_action_type)
