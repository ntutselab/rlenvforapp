import string

import gensim
import numpy as np

from RLEnvForApp.logger.logger import Logger


class FastTextSingleton:
    _instance = None

    @staticmethod
    def getInstance():
        if FastTextSingleton._instance is None:
            FastTextSingleton()
        return FastTextSingleton._instance

    def __init__(self):
        if FastTextSingleton._instance is not None:
            raise Exception('only one instance can exist')
        else:
            Logger().info("init FastTextSingleton ...")
            self._id = id(self)
            self._model = gensim.models.wrappers.FastText.load_fasttext_format(model_file='model/fasttext/cc.en.300.bin')
            # self._model = gensim.models.KeyedVectors.load_word2vec_format(fname='model/fasttext/wiki-news-300d-1M.vec')  # smaller model
            # self._model = gensim.models.KeyedVectors.load_word2vec_format(fname='model/fasttext/crawl-300d-2M.vec')  # smaller model
            FastTextSingleton._instance = self
            Logger().info("done")

    def getId(self):
        return self._id

    def getWordsVector(self, words: list):
        vectors = []
        for word in words:
            word = self.removeSymbols(word)
            if word.strip() == '':
                continue
            vectors.append(self.getWordVector(word))
        return vectors

    def getWordVector(self, word: str):
        word = self.removeSymbols(word)
        if word != "":
            vector = self._model[word]
        else:
            vector = np.zeros(300)
        return vector

    def removeSymbols(self, word: str):
        symbolRemoved = word.translate(str.maketrans('', '', string.punctuation)).strip()  # remove symbols
        return symbolRemoved
