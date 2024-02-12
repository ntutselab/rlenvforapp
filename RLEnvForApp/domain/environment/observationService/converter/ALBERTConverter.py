from RLEnvForApp.domain.environment.observationService.converter import \
    IConverter
from RLEnvForApp.domain.environment.observationService.converter.ALBERTTokenizerSingleton import \
    ALBERTTokenizerSingleton


class ALBERTConverter(IConverter):
    def __init__(self):
        super().__init__()

    def _convert_to_list_feature(self, stateElement) -> []:
        stateElement = stateElement.lower()
        tokenIds = ALBERTTokenizerSingleton.get_instance().get_token_ids(stateElement)
        return tokenIds
