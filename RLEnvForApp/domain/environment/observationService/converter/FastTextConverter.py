from RLEnvForApp.domain.environment.observationService.converter.FastTextSingleton import \
    FastTextSingleton
from RLEnvForApp.domain.environment.observationService.converter.IConverter import \
    IConverter


class FastTextConverter(IConverter):
    def __init__(self):
        super().__init__()
        FastTextSingleton.get_instance()

    def _convert_to_list_feature(self, state_element) -> []:
        word = state_element.lower()
        return FastTextSingleton.get_instance().get_word_vector(word=word)
