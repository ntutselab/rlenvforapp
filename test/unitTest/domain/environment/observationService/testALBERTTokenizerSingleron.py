import unittest

from RLEnvForApp.domain.environment.observationService.converter.ALBERTTokenizerSingleton import \
    ALBERTTokenizerSingleton


class TestBERTTokenizerSingleton(unittest.TestCase):
    def set_up(self) -> None:
        self.tokenizer = ALBERTTokenizerSingleton.get_instance()

    def test_get_id(self):
        self.assertEqual(self.tokenizer.get_id(),
                         ALBERTTokenizerSingleton.get_instance().get_id())

    def test_get_token_ids(self):
        word_sequence: str = "word sequence test, yes."
        word_sequence_token_ids: [] = [833, 4030, 1289, 15, 1643, 9]
        self.assertEqual(len(word_sequence_token_ids),
                         len(self.tokenizer.get_token_ids(word_sequence)))
        self.assertEqual(
            word_sequence_token_ids,
            self.tokenizer.get_token_ids(word_sequence))
