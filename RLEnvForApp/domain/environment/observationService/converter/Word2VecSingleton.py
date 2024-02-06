import string

import gensim
import numpy as np

from RLEnvForApp.logger.logger import Logger


class Word2VecSingleton:
    _instance = None

    @staticmethod
    def getInstance():
        if Word2VecSingleton._instance is None:
            Word2VecSingleton()
        return Word2VecSingleton._instance

    def __init__(self):
        if Word2VecSingleton._instance is not None:
            raise Exception('only one instance can exist')
        else:
            Logger().info("init Word2VecSingleton ...")
            self._id = id(self)
            self._model = gensim.models.KeyedVectors.load_word2vec_format(
                'model/word2vector/GoogleNews-vectors-negative300.bin', binary=True)
            Word2VecSingleton._instance = self
            Logger().info("done")

    def getId(self):
        return self._id

    def getWordsVector(self, words: list):
        vector = [0] * 300
        for word in words:
            word = self.removeSymbols(word)
            if word == '' or word == ' ':
                continue
            vector += self.getWordVector(word)
        return vector

    def getWordVector(self, word: str):
        word = self.removeSymbols(word)
        if self.isInVocab(word):
            vector = self._model[word]
        else:
            vector = np.zeros(300)
        return vector

    def isInVocab(self, word: str):
        word = self.removeSymbols(word)
        if word in self._model.vocab:
            return True
        else:
            Logger().info("Word2VecWarning: '" + word + "' is not in the vocab")
            return False

    def removeSymbols(self, word: str):
        # print("Original:", word, ", SymbolRemoved:", word.translate(str.maketrans('', '', string.punctuation)).strip())
        return word.translate(str.maketrans('', '', string.punctuation)).strip()  # remove symbols
