from RLEnvForApp.domain.environment.observationService.converter.IConverter import \
    IConverter


class ASCIIConverter(IConverter):
    def __init__(self):
        super().__init__()

    def _convert_to_list_feature(self, state_element) -> []:
        list_code_coverage_vector = []

        for char in state_element:
            list_code_coverage_vector.append(ord(char))

        return list_code_coverage_vector
