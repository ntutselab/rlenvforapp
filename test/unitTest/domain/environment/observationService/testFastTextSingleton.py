import unittest

from RLEnvForApp.domain.environment.observationService.converter.FastTextSingleton import \
    FastTextSingleton


class testFastTextSingleton(unittest.TestCase):
    def set_up(self) -> None:
        self.model = FastTextSingleton.get_instance()

    def test_get_id(self):
        self.assertEqual(
            self.model.get_id(),
            FastTextSingleton.get_instance().get_id())

    def test_get_word_vector(self):
        word_token: str = "word"
        self.assertTrue(300, len(self.model.get_word_vector(word_token)))

    def test_get_words_vector(self):
        word_tokens: [] = ["word", "sequence"]
        self.assertTrue(300, len(self.model.get_words_vector(word_tokens)))
