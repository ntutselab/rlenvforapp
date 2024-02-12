from RLEnvForApp.domain.environment.state import State


class IObservationService:
    def __init__(self):
        pass

    def get_observation(self, state: State):
        pass

    def get_original_observation(self, state: State) -> dict:
        return {}

    def get_observation_dictionary(self, observation: [int]):
        pass

    def get_observation_size(self):
        pass
