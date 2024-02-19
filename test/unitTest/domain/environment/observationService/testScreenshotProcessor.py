import os
import unittest

import numpy as np

from RLEnvForApp.domain.environment.observationService.converter.ScreenshotPreprocessor import \
    ScreenshotPreprocessor


class testScreenshotProcessor(unittest.TestCase):
    def setUp(self) -> None:
        self._savePath = './screenshot.png'
        self.imageArray = np.zeros((1920, 1080, 4))

    def tearDown(self) -> None:
        pass

    def testHappyPath(self):
        image_preprocessor = ScreenshotPreprocessor(self.imageArray, colorMode='grayscale', targetSize=(1024, 768))
        self.assertEqual(self._savePath, image_preprocessor._imagePath)
        self.assertEqual('grayscale', image_preprocessor._colorMode)
        self.assertEqual((1024, 768), image_preprocessor._targetSize)

        image_array = image_preprocessor.getImageArray()
        self.assertEqual((1024, 768, 1), image_array.shape)

        image_preprocessor.saveImage(self._savePath)
        self.assertTrue(os.path.exists(self._savePath))
