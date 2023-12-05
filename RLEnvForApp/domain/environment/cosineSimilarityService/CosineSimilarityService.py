import numpy as np
import tensorflow as tf

class CosineSimilarityService:
    @staticmethod
    def getCosineSimilarity(vector1, vector2):
        if all(v == 0 for v in vector1) or all(v == 0 for v in vector2):
            return -1.0
        return np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2))

    @staticmethod
    def getTokens(word: str):
        return tf.keras.preprocessing.text.text_to_word_sequence(word, filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n',
                                                                 lower=True, split=' ')
