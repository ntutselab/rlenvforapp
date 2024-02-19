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
        self._inputTypeList: list = inputSpace.inputTypes
        self._inputTypeListLength = len(inputSpace.inputTypes)

    def setup_model(self):
        pass

    def learn(self, total_timesteps, callback=None,
              log_interval=100, tb_log_name="run", reset_num_timesteps=True, replay_wrapper=None):

        observation = self._env.reset()
        for i in range(0, total_timesteps):
            action = self.predict(observation=observation)
            observation, rewards, isDone, info = self._env.step(action)

    def predict(self, observation, state=None, mask=None, deterministic=False):
        # return str(self._env.action_space.sample()), None  # random select
        return self.selectActionByCosineSimilarity(observation), None

    def action_probability(self, observation, state=None, mask=None, actions=None, logp=False):
        pass

    def save(self, save_path, cloudpickle=False):
        pass

    @classmethod
    def load(cls, load_path, env=None, custom_objects=None, **kwargs):
        pass

    def selectActionByCosineSimilarity(self, observation):
        similarity = 0.0
        inputTypeIndex = None

        autOperator = self._env.env_method(method_name="getAUTOperator")[0]
        focusedAppElement = autOperator.getFocusedAppElement()

        if not focusedAppElement:
            return str(self._env.action_space.sample())

        tagName = focusedAppElement.getTagName()
        elementType = focusedAppElement.getType()
        if tagName == "button" or tagName == "a" or \
                (tagName == 'input' and (
                    elementType == 'submit' or elementType == 'image' or elementType == 'checkbox' or elementType == 'radio')):
            similarity = 1.0
            inputTypeIndex = 0
            for appElement in autOperator.getAllSelectedAppElements():
                if appElement == focusedAppElement:
                    continue
                if not appElement.getValue():
                    similarity = 0.0
                    inputTypeIndex = None

        for i in range(0, self._inputTypeListLength):
            category = self._inputTypeList[i]

            categoryListTokens = inputSpace.CategoryListSingleton.getInstance().getCategoryExtendList()[
                category]
            categoryListTokens.append(category)

            # vectorization whole String
            categoryListVector = FastTextSingleton.getInstance().getWordsVector(categoryListTokens)
            elementLabelVector = np.array(observation[:, :300, :].reshape(300))

            labelCosineSimilarity = -1
            if categoryListVector:
                for categoryVector in categoryListVector:
                    labelCosineSimilarity = max(
                        CosineSimilarityService.getCosineSimilarity(categoryVector, elementLabelVector), labelCosineSimilarity)

            if np.isnan(labelCosineSimilarity):
                continue
            else:
                if labelCosineSimilarity > similarity:
                    similarity = labelCosineSimilarity
                    inputTypeIndex = i

        if inputTypeIndex is None:
            return str(self._env.action_space.sample())

        actionList = list(range(self._inputTypeListLength))
        probabilities = [1 / self._inputTypeListLength for _ in actionList]
        probabilities[inputTypeIndex] *= 30
        probabilities = [float(weight) / sum(actionList) for weight in probabilities]
        randomActionType = random.choices(actionList, probabilities)[0]

        Logger().info(f"Similarity: {similarity}, Action: {self._inputTypeList[inputTypeIndex]}")
        Logger().info(f"Final action: {self._inputTypeList[randomActionType]}")

        return str(randomActionType)
