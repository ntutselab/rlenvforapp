import tensorflow as tf


class ScreenshotPreprocessor:
    def __init__(self, imageArray, colorMode='rgb', targetSize=None):
        self._imageArray = imageArray
        self._colorMode = ''
        self._targetSize = None
        self._image = tf.keras.preprocessing.image.array_to_img(
            self._imageArray, data_format="channels_last")
        self._imagePath = './screenshot.png'

        self.loadImage(colorMode, targetSize)
        self._preprocessImage()

    def loadImage(self, colorMode='rgb', targetSize=None):
        tf.keras.preprocessing.image.save_img(
            self._imagePath, self._imageArray)

        self._colorMode = colorMode
        self._targetSize = targetSize
        if targetSize is None:
            self._image = tf.keras.preprocessing.image.load_img(
                path=self._imagePath, color_mode=colorMode)
        else:
            self._image = tf.keras.preprocessing.image.load_img(
                path=self._imagePath, color_mode=colorMode, target_size=targetSize)

    def getImageArray(self):
        return self._imageArray

    def saveImage(self, save_path="./"):
        tf.keras.preprocessing.image.save_img(save_path, self._imageArray)

    def _preprocessImage(self):
        self._imageArray = tf.keras.preprocessing.image.img_to_array(
            self._image)
