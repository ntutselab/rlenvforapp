from RLEnvForApp.domain.environment.observationService.converter import \
    IConverter
from RLEnvForApp.domain.environment.observationService.converter.BERTTokenizerSingleton import \
    BERTTokenizerSingleton


class BERTConverter(IConverter):
    def __init__(self):
        super().__init__()

    def _convert_to_list_feature(self, stateElement) -> []:
        stateElement = stateElement.lower()
        tokens = BERTTokenizerSingleton.get_instance().get_tokens(stateElement)
        tokenIds = BERTTokenizerSingleton.get_instance().get_token_ids(tokens)

        return tokenIds
