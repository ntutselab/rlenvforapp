import numpy as np

from RLEnvForApp.domain.environment import inputSpace
from RLEnvForApp.domain.environment.cosineSimilarityService.CosineSimilarityService import \
    CosineSimilarityService
from RLEnvForApp.domain.environment.episodeHandler.IEpisodeHandler import IEpisodeHandler
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

    def calculateReward(self, episodeHandler: IEpisodeHandler):
        previousState: State = episodeHandler.getAllState()[-2]

        if previousState.getInteractedElement() is None:
            self._logger.info('Interacted element is none, reward: 0')
            return 0

        if previousState.getActionType() == "input":
            self._logger.info('Calculating input reward...')
            return self._getInputValueReward(previousState=previousState)

        return 0

    def _getInputValueReward(self, previousState: State):
        elementLabel = previousState.getOriginalObservation()["labelName"]

        if not elementLabel:
            self._logger.info("Label is empty")
            return 0.0

        inputCategory = self._inputTypeList[previousState.getActionNumber()]

        categoryListTokens = inputSpace.CategoryListSingleton.getInstance().getCategoryExtendList()[inputCategory]
        categoryListTokens.append(inputCategory)

        # vectorization whole String
        categoryListVector = FastTextSingleton.getInstance().getWordsVector(categoryListTokens)
        elementLabelVector = FastTextSingleton.getInstance().getWordVector(word=elementLabel)

        labelCosineSimilarity = -1
        if categoryListVector:
            for categoryVector in categoryListVector:
                labelCosineSimilarity = max(
                    CosineSimilarityService.getCosineSimilarity(categoryVector, elementLabelVector),
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

    def getCosineSimilarityText(self) -> str:
        return self._cosineSimilarityText
