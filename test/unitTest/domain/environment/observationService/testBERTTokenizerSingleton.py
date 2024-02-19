import unittest

from RLEnvForApp.domain.environment.observationService.converter.BERTTokenizerSingleton import \
    BERTTokenizerSingleton


class testBERTTokenizerSingleton(unittest.TestCase):
    def setUp(self) -> None:
        self.tokenizer = BERTTokenizerSingleton.getInstance()

    def testGetId(self):
        self.assertEqual(self.tokenizer.getId(), BERTTokenizerSingleton.getInstance().getId())

    def testGetTokens(self):
        word_sequence: str = "word sequence test, yes."
        word_sequence_token: [] = ["word", "sequence", "test", ",", "yes", "."]
        self.assertEqual(word_sequence_token, self.tokenizer.getTokens(word_sequence))

    def testGetTokenIds(self):
        word_sequence_token: [] = ["word", "sequence", "test", ",", "yes", "."]
        word_sequence_token_ids: [] = [2773, 5537, 3231, 1010, 2748, 1012]
        self.assertEqual(len(word_sequence_token_ids), len(
            self.tokenizer.getTokenIds(word_sequence_token)))
        self.assertEqual(word_sequence_token_ids, self.tokenizer.getTokenIds(word_sequence_token))
