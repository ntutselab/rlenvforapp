from RLEnvForApp.domain.environment.observationService.converter.IConverter import IConverter
from RLEnvForApp.domain.environment.observationService.converter.Word2VecSingleton import Word2VecSingleton
from RLEnvForApp.domain.environment.observationService.converter.BERTTokenizerSingleton import BERTTokenizerSingleton


class Word2VecConverter(IConverter):
    def __init__(self):
        super().__init__()
        Word2VecSingleton.getInstance()

    def _convertToListFeature(self, stateElement) -> []:
        word_sequence = stateElement.lower()
        # print("word_sequence=", word_sequence) # debug
        tokens = BERTTokenizerSingleton.getInstance().getTokens(word_sequence)
        return Word2VecSingleton.getInstance().getWordsVector(words=tokens)
