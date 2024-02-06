from RLEnvForApp.domain.environment.observationService.converter.ScreenshotPreprocessor import ScreenshotPreprocessor
from RLEnvForApp.domain.environment.observationService.converter import IConverter


class ScreenshotConverter(IConverter):
    def __init__(self):
        super().__init__()

    def _convertToListFeature(self, stateElement) -> []:
        screenshotPreprocessor = ScreenshotPreprocessor(
            stateElement, colorMode='grayscale', targetSize=(331, 916))
        return screenshotPreprocessor.getImageArray()
