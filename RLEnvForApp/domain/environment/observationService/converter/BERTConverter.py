from RLEnvForApp.domain.environment.observationService.converter import \
    IConverter
from RLEnvForApp.domain.environment.observationService.converter.BERTTokenizerSingleton import \
    BERTTokenizerSingleton


class BERTConverter(IConverter):
    def __init__(self):
        super().__init__()

    def _convert_to_list_feature(self, state_element) -> []:
        state_element = state_element.lower()
        tokens = BERTTokenizerSingleton.get_instance().get_tokens(state_element)
        token_ids = BERTTokenizerSingleton.get_instance().get_token_ids(tokens)

        return token_ids
