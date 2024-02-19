from RLEnvForApp.domain.environment.observationService.converter.OneHotConverter import \
    OneHotConverter
from RLEnvForApp.domain.environment.observationService.IObservationService import \
    IObservationService
from RLEnvForApp.domain.environment.state import State


class DefaultForTestObservationService(IObservationService):
    def __init__(self):
        super().__init__()
        self._domLength = 0
        self._oneHotLength = 150
        self._oneHotCoveredNumber = 300

    def getObservation(self, state: State):
        onehotConverter = OneHotConverter(coveredNumber=self._oneHotCoveredNumber)
        listFocusOneHot = onehotConverter.convert(
            stateElement=state.getFocusVector(), length=self._oneHotLength)
        return listFocusOneHot

    def getObservationDictionary(self, observation: [int]):
        observationDictionary = {}
        observationDictionary["listDom"] = observation[0:130100]
        observationDictionary["listFocusOneHot"] = observation[130100:]
        return observationDictionary

    def getObservationSize(self):
        return (1, self._domLength + self._oneHotLength * 1, 1)
