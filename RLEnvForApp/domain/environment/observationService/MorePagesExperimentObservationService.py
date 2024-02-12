
import numpy as np

from RLEnvForApp.domain.environment import inputSpace
from RLEnvForApp.domain.environment.cosineSimilarityService.CosineSimilarityService import CosineSimilarityService
from RLEnvForApp.domain.environment.observationService.IObservationService import IObservationService
from RLEnvForApp.domain.environment.observationService.converter.FastTextConverter import FastTextConverter
from RLEnvForApp.domain.environment.observationService.converter.FastTextSingleton import FastTextSingleton
from RLEnvForApp.domain.environment.state import State


class MorePagesExperimentObservationService(IObservationService):
    def __init__(self):
        super().__init__()
        self._textConverter = FastTextConverter()

    def getObservation(self, state: State):
        observationDict = self.getOriginalObservation(state=state)

        listLabelName = self._textConverter.convert(stateElement=observationDict["labelName"])
        listTagName = self._textConverter.convert(stateElement=observationDict["tagName"])
        listType = self._textConverter.convert(stateElement=observationDict["type"])

        wordsObservation = [*listLabelName, *listTagName, *listType]
        return wordsObservation, observationDict

    def getOriginalObservation(self, state: State):
        observationDict = {}
        labelName = ""
        tagName = ""
        elementType = ""

        if True in state.getFocusVector():
            focusedIndex = state.getFocusVector().index(True)
            focusedElement = state.getAllSelectedAppElements()[focusedIndex]
            labelName = self._getElementLabelBySimilarity(state)
            tagName = focusedElement.getTagName().lower()
            elementType = focusedElement.getType().lower()
        observationDict["labelName"] = labelName
        observationDict["tagName"] = tagName
        observationDict["type"] = elementType
        return observationDict

    def getObservationDictionary(self, observation: [int]):
        pass

    def getObservationSize(self):
        return (1, 300 * 3, 1)

    def _isFormComplete(self, state: State):
        complete = True
        for appElement in state.getAllSelectedAppElements():
            if appElement.getValue() == "":
                complete = False
        return complete

    def _getElementLabelBySimilarity(self, state: State):
        elementName = state.getInteractedElement().getName().lower()
        elementLabel = state.getInteractedElementLabel().lower()
        elementPlaceholder = state.getInteractedElementPlaceholder().lower()
        if not elementLabel:
            if elementPlaceholder:
                elementLabel = elementPlaceholder
            else:
                elementLabel = elementName

        if not elementLabel:
            return ""

        elementLabelTokens = CosineSimilarityService.getTokens(elementLabel)
        elementLabelVectors = list(
            map(FastTextSingleton.getInstance().getWordVector, elementLabelTokens))
        categoryVectors = list(
            map(FastTextSingleton.getInstance().getWordVector, inputSpace.inputTypes))

        labelVectorSimilarities = [0] * len(elementLabelTokens)
        for index, elementLabelVector in enumerate(elementLabelVectors):
            labelVectorSimilarity = 0
            for categoryVector in categoryVectors:
                labelVectorSimilarity = max(
                    CosineSimilarityService.getCosineSimilarity(
                        categoryVector, elementLabelVector), labelVectorSimilarity)
            labelVectorSimilarities[index] = labelVectorSimilarity

        totalSum = sum(labelVectorSimilarities)
        labelVectorSimilarities = [x / totalSum for x in labelVectorSimilarities]
        elementLabelToken = np.random.choice(
            elementLabelTokens, size=1, p=labelVectorSimilarities)[0]

        return elementLabelToken
