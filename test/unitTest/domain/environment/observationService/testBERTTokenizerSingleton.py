import unittest

from RLEnvForApp.domain.environment.observationService.converter.BERTTokenizerSingleton import \
    BERTTokenizerSingleton


class TestBERTTokenizerSingleton(unittest.TestCase):
    def set_up(self) -> None:
        self.tokenizer = BERTTokenizerSingleton.get_instance()

    def test_get_id(self):
        self.assertEqual(self.tokenizer.get_id(),
                         BERTTokenizerSingleton.get_instance().get_id())

    def test_get_tokens(self):
        word_sequence: str = "word sequence test, yes."
        word_sequence_token: [] = ["word", "sequence", "test", ",", "yes", "."]
        self.assertEqual(word_sequence_token,
                         self.tokenizer.get_tokens(word_sequence))

    def test_get_token_ids(self):
        word_sequence_token: [] = ["word", "sequence", "test", ",", "yes", "."]
        word_sequence_token_ids: [] = [2773, 5537, 3231, 1010, 2748, 1012]
        self.assertEqual(len(word_sequence_token_ids), len(
            self.tokenizer.get_token_ids(word_sequence_token)))
        self.assertEqual(word_sequence_token_ids,
                         self.tokenizer.get_token_ids(word_sequence_token))
