from RLEnvForApp.domain.environment.observationService.converter.IConverter import \
    IConverter


class OneHotConverter(IConverter):
    def __init__(self, coveredNumber: int):
        self._covered_number = coveredNumber
        super().__init__()

    def _convert_to_list_feature(self, state_element) -> []:
        list_one_hot: [int] = []
        for i in state_element:
            if i:
                list_one_hot.append(self._covered_number)
            else:
                list_one_hot.append(0)
        return list_one_hot
