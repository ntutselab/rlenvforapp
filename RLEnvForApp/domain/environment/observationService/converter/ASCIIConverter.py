from RLEnvForApp.domain.environment.observationService.converter.IConverter import \
    IConverter


class ASCIIConverter(IConverter):
    def __init__(self):
        super().__init__()

    def _convert_to_list_feature(self, stateElement) -> []:
        listCodeCoverageVector = []

        for char in stateElement:
            listCodeCoverageVector.append(ord(char))

        return listCodeCoverageVector
