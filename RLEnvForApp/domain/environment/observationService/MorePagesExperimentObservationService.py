
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
        self._text_converter = FastTextConverter()

    def get_observation(self, state: State):
        observation_dict = self.get_original_observation(state=state)

        list_label_name = self._text_converter.convert(
            state_element=observation_dict["labelName"])
        list_tag_name = self._text_converter.convert(
            state_element=observation_dict["tagName"])
        list_type = self._text_converter.convert(
            state_element=observation_dict["type"])

        words_observation = [*list_label_name, *list_tag_name, *list_type]
        return words_observation, observation_dict

    def get_original_observation(self, state: State):
        observation_dict = {}
        label_name = ""
        tag_name = ""
        element_type = ""

        if True in state.get_focus_vector():
            focusedIndex = state.get_focus_vector().index(True)
            focusedElement = state.get_all_selected_app_elements()[focusedIndex]
            label_name = self._get_element_label_by_similarity(state)
            tag_name = focusedElement.get_tag_name().lower()
            element_type = focusedElement.get_type().lower()
        observation_dict["labelName"] = label_name
        observation_dict["tagName"] = tag_name
        observation_dict["type"] = element_type
        return observation_dict

    def get_observation_dictionary(self, observation: [int]):
        pass

    def get_observation_size(self):
        return (1, 300 * 3, 1)

    def _is_form_complete(self, state: State):
        complete = True
        for app_element in state.get_all_selected_app_elements():
            if app_element.get_value() == "":
                complete = False
        return complete

    def _get_element_label_by_similarity(self, state: State):
        element_name = state.get_interacted_element().get_name().lower()
        element_label = state.get_interacted_element_label().lower()
        element_placeholder = state.get_interacted_element_placeholder().lower()
        if not element_label:
            if element_placeholder:
                element_label = element_placeholder
            else:
                element_label = element_name

        if not element_label:
            return ""

        element_label_tokens = CosineSimilarityService.get_tokens(element_label)
        element_label_vectors = list(
            map(FastTextSingleton.get_instance().getWordVector, element_label_tokens))
        category_vectors = list(
            map(FastTextSingleton.get_instance().getWordVector, inputSpace.inputTypes))

        label_vector_similarities = [0] * len(element_label_tokens)
        for index, element_label_vector in enumerate(element_label_vectors):
            labelVectorSimilarity = 0
            for categoryVector in category_vectors:
                labelVectorSimilarity = max(
                    CosineSimilarityService.get_cosine_similarity(
                        categoryVector, element_label_vector), labelVectorSimilarity)
            label_vector_similarities[index] = labelVectorSimilarity

        total_sum = sum(label_vector_similarities)
        label_vector_similarities = [
            x / total_sum for x in label_vector_similarities]
        element_label_token = np.random.choice(
            element_label_tokens, size=1, p=label_vector_similarities)[0]

        return element_label_token
