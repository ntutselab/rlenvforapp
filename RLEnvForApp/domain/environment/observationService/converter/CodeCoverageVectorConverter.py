from RLEnvForApp.domain.environment.observationService.converter.IConverter import \
    IConverter


class CodeCoverageVectorConverter(IConverter):
    def __init__(self):
        super().__init__()

    def _convert_to_list_feature(self, stateElement) -> []:
        listCodeCoverageVector = []

        for i in stateElement:
            if i:
                listCodeCoverageVector.append(1)
            else:
                listCodeCoverageVector.append(0)

        return listCodeCoverageVector
