from RLEnvForApp.domain.environment.observationService.converter import \
    IConverter
from RLEnvForApp.domain.environment.observationService.converter.ScreenshotPreprocessor import \
    ScreenshotPreprocessor


class ScreenshotConverter(IConverter):
    def __init__(self):
        super().__init__()

    def _convert_to_list_feature(self, state_element) -> []:
        screenshot_preprocessor = ScreenshotPreprocessor(
            state_element, colorMode='grayscale', targetSize=(331, 916))
        return screenshot_preprocessor.get_image_array()
