from RLEnvForApp.domain.environment.observationService.converter import \
    IConverter
from RLEnvForApp.domain.environment.observationService.converter.ALBERTTokenizerSingleton import \
    ALBERTTokenizerSingleton


class ALBERTConverter(IConverter):
    def __init__(self):
        super().__init__()

    def _convert_to_list_feature(self, state_element) -> []:
        state_element = state_element.lower()
        token_ids = ALBERTTokenizerSingleton.get_instance().get_token_ids(state_element)
        return token_ids
