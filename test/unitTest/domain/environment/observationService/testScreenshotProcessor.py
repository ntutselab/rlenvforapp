import os
import unittest

import numpy as np

from RLEnvForApp.domain.environment.observationService.converter.ScreenshotPreprocessor import \
    ScreenshotPreprocessor


class testScreenshotProcessor(unittest.TestCase):
    def set_up(self) -> None:
        self._save_path = './screenshot.png'
        self.image_array = np.zeros((1920, 1080, 4))

    def tear_down(self) -> None:
        pass

    def test_happy_path(self):
        image_preprocessor = ScreenshotPreprocessor(
            self.image_array, colorMode='grayscale', targetSize=(1024, 768))
        self.assertEqual(self._save_path, image_preprocessor._image_path)
        self.assertEqual('grayscale', image_preprocessor._color_mode)
        self.assertEqual((1024, 768), image_preprocessor._target_size)

        image_array = image_preprocessor.get_image_array()
        self.assertEqual((1024, 768, 1), image_array.shape)

        image_preprocessor.save_image(self._save_path)
        self.assertTrue(os.path.exists(self._save_path))
