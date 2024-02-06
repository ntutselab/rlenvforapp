from RLEnvForApp.domain.environment.state import State


class IObservationService:
    def __init__(self):
        pass

    def getObservation(self, state: State):
        pass

    def getOriginalObservation(self, state: State) -> dict:
        return {}

    def getObservationDictionary(self, observation: [int]):
        pass

    def getObservationSize(self):
        pass
