
import numpy as np

from RLEnvForApp.domain.environment import inputSpace
from RLEnvForApp.domain.environment.cosineSimilarityService.CosineSimilarityService import \
    CosineSimilarityService
from RLEnvForApp.domain.environment.observationService.converter.FastTextConverter import \
    FastTextConverter
from RLEnvForApp.domain.environment.observationService.converter.FastTextSingleton import \
    FastTextSingleton
from RLEnvForApp.domain.environment.observationService.IObservationService import \
    IObservationService
from RLEnvForApp.domain.environment.state import State


class MorePagesExperimentObservationService(IObservationService):
    def __init__(self):
        super().__init__()
        self._textConverter = FastTextConverter()

    def get_observation(self, state: State):
        observationDict = self.get_original_observation(state=state)

        listLabelName = self._textConverter.convert(
            stateElement=observationDict["labelName"])
        listTagName = self._textConverter.convert(
            stateElement=observationDict["tagName"])
        listType = self._textConverter.convert(
            stateElement=observationDict["type"])

        wordsObservation = [*listLabelName, *listTagName, *listType]
        return wordsObservation, observationDict

    def get_original_observation(self, state: State):
        observationDict = {}
        labelName = ""
        tagName = ""
        elementType = ""

        if True in state.get_focus_vector():
            focusedIndex = state.get_focus_vector().index(True)
            focusedElement = state.get_all_selected_app_elements()[focusedIndex]
            labelName = self._get_element_label_by_similarity(state)
            tagName = focusedElement.get_tag_name().lower()
            elementType = focusedElement.get_type().lower()
        observationDict["labelName"] = labelName
        observationDict["tagName"] = tagName
        observationDict["type"] = elementType
        return observationDict

    def get_observation_dictionary(self, observation: [int]):
        pass

    def get_observation_size(self):
        return (1, 300 * 3, 1)

    def _is_form_complete(self, state: State):
        complete = True
        for appElement in state.get_all_selected_app_elements():
            if appElement.get_value() == "":
                complete = False
        return complete

    def _get_element_label_by_similarity(self, state: State):
        elementName = state.get_interacted_element().get_name().lower()
        elementLabel = state.get_interacted_element_label().lower()
        elementPlaceholder = state.get_interacted_element_placeholder().lower()
        if not elementLabel:
            if elementPlaceholder:
                elementLabel = elementPlaceholder
            else:
                elementLabel = elementName

        if not elementLabel:
            return ""

        elementLabelTokens = CosineSimilarityService.get_tokens(elementLabel)
        elementLabelVectors = list(
            map(FastTextSingleton.get_instance().getWordVector, elementLabelTokens))
        categoryVectors = list(
            map(FastTextSingleton.get_instance().getWordVector, inputSpace.inputTypes))

        labelVectorSimilarities = [0] * len(elementLabelTokens)
        for index, elementLabelVector in enumerate(elementLabelVectors):
            labelVectorSimilarity = 0
            for categoryVector in categoryVectors:
                labelVectorSimilarity = max(
                    CosineSimilarityService.get_cosine_similarity(
                        categoryVector, elementLabelVector), labelVectorSimilarity)
            labelVectorSimilarities[index] = labelVectorSimilarity

        totalSum = sum(labelVectorSimilarities)
        labelVectorSimilarities = [
            x / totalSum for x in labelVectorSimilarities]
        elementLabelToken = np.random.choice(
            elementLabelTokens, size=1, p=labelVectorSimilarities)[0]

        return elementLabelToken
