from RLEnvForApp.domain.environment.observationService.converter import IConverter
from RLEnvForApp.domain.environment.observationService.converter.BERTTokenizerSingleton import BERTTokenizerSingleton


class BERTConverter(IConverter):
    def __init__(self):
        super().__init__()

    def _convertToListFeature(self, stateElement) -> []:
        stateElement = stateElement.lower()
        tokens = BERTTokenizerSingleton.getInstance().getTokens(stateElement)
        tokenIds = BERTTokenizerSingleton.getInstance().getTokenIds(tokens)

        return tokenIds
