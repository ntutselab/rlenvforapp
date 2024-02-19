from RLEnvForApp.domain.environment.observationService.converter import IConverter
from RLEnvForApp.domain.environment.observationService.converter.ALBERTTokenizerSingleton import \
    ALBERTTokenizerSingleton


class ALBERTConverter(IConverter):
    def __init__(self):
        super().__init__()

    def _convertToListFeature(self, stateElement) -> []:
        stateElement = stateElement.lower()
        tokenIds = ALBERTTokenizerSingleton.getInstance().getTokenIds(stateElement)
        return tokenIds
