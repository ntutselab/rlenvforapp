import os
import bert
import sentencepiece as spm

from RLEnvForApp.logger.logger import Logger


class ALBERTTokenizerSingleton:
    _instance = None

    @staticmethod
    def getInstance():
        if ALBERTTokenizerSingleton._instance is None:
            ALBERTTokenizerSingleton()
        return ALBERTTokenizerSingleton._instance

    def __init__(self):
        if ALBERTTokenizerSingleton._instance is not None:
            raise Exception('only one instance can exist')
        else:
            Logger().info("init ALBERTTokenizerSingleton ...")
            self._id = id(self)
            self._model_dir = "model/albert/albert_base"
            self._spm_model = os.path.join(self._model_dir, "30k-clean.model")
            self._sp = spm.SentencePieceProcessor()
            self._sp.load(self._spm_model)
            ALBERTTokenizerSingleton._instance = self
            Logger().info("done")

    def getId(self):
        return self._id

    def getTokenIds(self, sentence) -> []:
        processed_word = bert.albert_tokenization.preprocess_text(sentence.lower(), lower=True)
        return bert.albert_tokenization.encode_ids(self._sp, processed_word)
