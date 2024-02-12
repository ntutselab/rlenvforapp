from RLEnvForApp.domain.environment.observationService.converter.IConverter import IConverter
from RLEnvForApp.domain.environment.observationService.converter.FastTextSingleton import FastTextSingleton


class FastTextConverter(IConverter):
    def __init__(self):
        super().__init__()
        FastTextSingleton.getInstance()

    def _convertToListFeature(self, stateElement) -> []:
        word = stateElement.lower()
        return FastTextSingleton.getInstance().getWordVector(word=word)
