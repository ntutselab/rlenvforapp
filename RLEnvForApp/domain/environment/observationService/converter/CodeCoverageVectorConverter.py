from RLEnvForApp.domain.environment.observationService.converter.IConverter import \
    IConverter


class CodeCoverageVectorConverter(IConverter):
    def __init__(self):
        super().__init__()

    def _convert_to_list_feature(self, state_element) -> []:
        list_code_coverage_vector = []

        for i in state_element:
            if i:
                list_code_coverage_vector.append(1)
            else:
                list_code_coverage_vector.append(0)

        return list_code_coverage_vector
