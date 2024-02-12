from RLEnvForApp.domain.environment.observationService.converter.IConverter import \
    IConverter


class OneHotConverter(IConverter):
    def __init__(self, coveredNumber: int):
        self._coveredNumber = coveredNumber
        super().__init__()

    def _convertToListFeature(self, stateElement) -> []:
        listOneHot: [int] = []
        for i in stateElement:
            if i:
                listOneHot.append(self._coveredNumber)
            else:
                listOneHot.append(0)
        return listOneHot
