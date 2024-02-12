import unittest

from RLEnvForApp.domain.environment.observationService.converter.ALBERTTokenizerSingleton import \
    ALBERTTokenizerSingleton


class testBERTTokenizerSingleton(unittest.TestCase):
    def setUp(self) -> None:
        self.tokenizer = ALBERTTokenizerSingleton.getInstance()

    def testGetId(self):
        self.assertEqual(self.tokenizer.getId(), ALBERTTokenizerSingleton.getInstance().getId())

    def testGetTokenIds(self):
        word_sequence: str = "word sequence test, yes."
        word_sequence_token_ids: [] = [833, 4030, 1289, 15, 1643, 9]
        self.assertEqual(len(word_sequence_token_ids),
                         len(self.tokenizer.getTokenIds(word_sequence)))
        self.assertEqual(word_sequence_token_ids, self.tokenizer.getTokenIds(word_sequence))
