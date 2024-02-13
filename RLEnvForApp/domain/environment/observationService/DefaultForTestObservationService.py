from RLEnvForApp.domain.environment.observationService.converter.OneHotConverter import \
    OneHotConverter
from RLEnvForApp.domain.environment.observationService.IObservationService import \
    IObservationService
from RLEnvForApp.domain.environment.state import State


class DefaultForTestObservationService(IObservationService):
    def __init__(self):
        super().__init__()
        self._dom_length = 0
        self._one_hot_length = 150
        self._one_hot_covered_number = 300

    def get_observation(self, state: State):
        onehot_converter = OneHotConverter(
            coveredNumber=self._one_hot_covered_number)
        list_focus_one_hot = onehot_converter.convert(
            state_element=state.get_focus_vector(),
            length=self._one_hot_length)
        return list_focus_one_hot

    def get_observation_dictionary(self, observation: [int]):
        observation_dictionary = {}
        observation_dictionary["listDom"] = observation[0:130100]
        observation_dictionary["listFocusOneHot"] = observation[130100:]
        return observation_dictionary

    def get_observation_size(self):
        return (1, self._dom_length + self._one_hot_length * 1, 1)
