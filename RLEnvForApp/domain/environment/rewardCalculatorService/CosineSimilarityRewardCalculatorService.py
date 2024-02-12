
import numpy as np

from RLEnvForApp.domain.environment import inputSpace
from RLEnvForApp.domain.environment.episodeHandler.IEpisodeHandler import IEpisodeHandler
from RLEnvForApp.domain.environment.inputSpace import CategoryListSingleton, inputTypes
from RLEnvForApp.domain.environment.rewardCalculatorService.IRewardCalculatorService import IRewardCalculatorService
from RLEnvForApp.domain.environment.state.State import State
from RLEnvForApp.domain.environment.rewardCalculatorService.ActionIndicationService.IActionIndicationService import IActionIndicationService
from RLEnvForApp.domain.targetPage.TargetIndicationService.ITargetIndicationService import ITargetIndicationService
from RLEnvForApp.usecase.environment.executeAction.ActionIndicationService.CheckHTMLLogActionIndicationService import \
    CheckHTMLLogActionIndicationService
from RLEnvForApp.usecase.targetPage.ITargetIndicationService.HTMLLogIndicationService import HTMLLogIndicationService
from RLEnvForApp.domain.environment.cosineSimilarityService.CosineSimilarityService import CosineSimilarityService
from RLEnvForApp.domain.environment.observationService.converter.FastTextSingleton import FastTextSingleton
from RLEnvForApp.logger.logger import Logger


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

    def calculateReward(self, episodeHandler: IEpisodeHandler):
        previousState: State = episodeHandler.getAllState()[-2]

        if episodeHandler.isDone() and self._targetIndicationService.isConform(state=previousState):
            reward = self._episodeRewardCoefficient * \
                (1 / self._getEpisodeStepFraction(episodeHandler=episodeHandler))
            self._logger.info(f'Form submitted reward: {reward}')
            # self._updateCategoryList(previousState)
            return reward

        if previousState.getInteractedElement() is None:
            self._logger.info('Interacted element is none, reward: 0')
            return 0

        if self._actionIndicationService.isConform(state=previousState):
            if previousState.getActionType() == "input":
                # self._updateCategoryList(previousState)
                return self._getInputValueReward(previousState=previousState)

            if previousState.getActionType() == "click":
                return self._getClickReward(previousState=previousState)

            self._logger.info('Action type is not input or click. reward: -10')
            return -10
        else:
            self._logger.info('Category not match record, reward: -10')
            return -10

    def _getEpisodeStepFraction(self, episodeHandler: IEpisodeHandler):
        episodeStepFraction = 0

        numberOfState = episodeHandler.getNumberOfState()
        episodeStep = episodeHandler.getEpisodeStep()
        episodeStepFraction = (numberOfState - 1) / episodeStep
        return episodeStepFraction

    def _getInputValueReward(self, previousState: State):
        elementLabel = previousState.getOriginalObservation()["labelName"]

        if not elementLabel:
            self._logger.info("Label is empty")
            return 0.0

        inputCategory = self._inputTypeList[previousState.getActionNumber()]

        categoryListTokens = list(
            map(CosineSimilarityService.getTokens, inputSpace.CategoryListSingleton.getInstance().getCategoryExtendList()[inputCategory]))
        categoryListTokens.append(inputCategory)

        # vectorization whole String
        categoryListVector = list(
            map(FastTextSingleton.getInstance().getWordsVector, categoryListTokens))
        elementLabelVector = FastTextSingleton.getInstance().getWordVector(words=elementLabel)

        labelCosineSimilarity = -1
        if categoryListVector:
            for categoryVector in categoryListVector:
                labelCosineSimilarity = max(
                    CosineSimilarityService.getCosineSimilarity(
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

    def _getClickReward(self, previousState: State):
        tag = previousState.getInteractedElement().getTagName()
        elementType = previousState.getInteractedElement().getType()
        if tag == "button" or (tag == 'input' and (
                elementType == 'submit' or elementType == 'image' or elementType == 'checkbox' or elementType == 'radio')):
            rewardRevise = self._clickRewardCoefficient * 1
        elif tag == "a":
            rewardRevise = self._clickRewardCoefficient * -0.5
        else:
            rewardRevise = self._clickRewardCoefficient * -0.3

        self._logger.info(f'Click tag: {tag}, type: {elementType}')
        self._logger.info(f'Click reward: {self._inputRewardBaseLine + rewardRevise}')
        return self._inputRewardBaseLine + rewardRevise

    def _updateCategoryList(self, previousState: State):
        categoryExtendList = CategoryListSingleton.getInstance().getCategoryExtendList()

        category = inputTypes[previousState.getActionNumber()]
        if self._cosineSimilarityText != '' and self._cosineSimilarityText not in categoryExtendList[
                category]:
            categoryExtendList[category].append(self._cosineSimilarityText)
            self._logger.info(f"Append [{self._cosineSimilarityText}] to category: {category}")

        CategoryListSingleton.getInstance().setCategoryExtendList(categoryExtendList)

    def getCosineSimilarityText(self) -> str:
        return self._cosineSimilarityText
