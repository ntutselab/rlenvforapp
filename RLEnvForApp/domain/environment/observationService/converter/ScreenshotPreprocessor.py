import tensorflow as tf


class ScreenshotPreprocessor:
    def __init__(self, image_array, colorMode='rgb', targetSize=None):
        self._image_array = image_array
        self._color_mode = ''
        self._target_size = None
        self._image = tf.keras.preprocessing.image.array_to_img(
            self._image_array, data_format="channels_last")
        self._image_path = './screenshot.png'

        self.load_image(colorMode, targetSize)
        self._preprocess_image()

    def load_image(self, colorMode='rgb', targetSize=None):
        tf.keras.preprocessing.image.save_img(
            self._image_path, self._image_array)

        self._color_mode = colorMode
        self._target_size = targetSize
        if targetSize is None:
            self._image = tf.keras.preprocessing.image.load_img(
                path=self._image_path, color_mode=colorMode)
        else:
            self._image = tf.keras.preprocessing.image.load_img(
                path=self._image_path, color_mode=colorMode, target_size=targetSize)

    def get_image_array(self):
        return self._image_array

    def save_image(self, save_path="./"):
        tf.keras.preprocessing.image.save_img(save_path, self._image_array)

    def _preprocess_image(self):
        self._image_array = tf.keras.preprocessing.image.img_to_array(
            self._image)
