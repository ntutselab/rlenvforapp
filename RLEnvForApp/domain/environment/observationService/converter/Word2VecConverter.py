from RLEnvForApp.domain.environment.observationService.converter.BERTTokenizerSingleton import \
    BERTTokenizerSingleton
from RLEnvForApp.domain.environment.observationService.converter.IConverter import \
    IConverter
from RLEnvForApp.domain.environment.observationService.converter.Word2VecSingleton import \
    Word2VecSingleton


class Word2VecConverter(IConverter):
    def __init__(self):
        super().__init__()
        Word2VecSingleton.get_instance()

    def _convert_to_list_feature(self, state_element) -> []:
        word_sequence = state_element.lower()
        # print("word_sequence=", word_sequence) # debug
        tokens = BERTTokenizerSingleton.get_instance().get_tokens(word_sequence)
        return Word2VecSingleton.get_instance().get_words_vector(words=tokens)
