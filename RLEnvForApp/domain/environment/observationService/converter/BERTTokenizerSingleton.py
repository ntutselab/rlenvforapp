import os
import bert

from RLEnvForApp.logger.logger import Logger


class BERTTokenizerSingleton:
    _instance = None

    @staticmethod
    def getInstance():
        if BERTTokenizerSingleton._instance is None:
            BERTTokenizerSingleton()
        return BERTTokenizerSingleton._instance

    def __init__(self):
        if BERTTokenizerSingleton._instance is not None:
            raise Exception('only one instance can exist')
        else:
            Logger().info("init BERTTokenizerSingleton ...")
            self._id = id(self)
            self._model_dir = "model/bert/uncased_L-2_H-128_A-2"
            self._vocab_file = os.path.join(self._model_dir, "vocab.txt")
            self._tokenizer = bert.bert_tokenization.FullTokenizer(self._vocab_file, True)
            BERTTokenizerSingleton._instance = self
            Logger().info("done")

    def getId(self):
        return self._id

    def getTokens(self, sentence) -> []:
        sentence = sentence.lower()
        tokens = self._tokenizer.tokenize(sentence)
        return tokens

    def getTokenIds(self, tokens: []) -> []:
        return self._tokenizer.convert_tokens_to_ids(tokens)
