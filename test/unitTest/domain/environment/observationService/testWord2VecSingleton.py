import unittest

from RLEnvForApp.domain.environment.observationService.converter.Word2VecSingleton import \
    Word2VecSingleton


class testWord2VecSingleton(unittest.TestCase):
    def set_up(self) -> None:
        self.model = Word2VecSingleton.get_instance()

    def test_get_id(self):
        self.assertEqual(
            self.model.get_id(),
            Word2VecSingleton.get_instance().get_id())

    def test_is_in_vocab(self):
        word_token: str = "word"
        self.assertTrue(self.model.get_instance().is_in_vocab(word_token))
        self.assertFalse(self.model.get_instance().is_in_vocab("I_do_not_exist"))

    def test_get_word_vector(self):
        word_token: str = "word"
        self.assertTrue(300, len(self.model.get_word_vector(word_token)))

    def test_get_words_vector(self):
        word_tokens: [] = ["word", "sequence"]
        self.assertTrue(300, len(self.model.get_words_vector(word_tokens)))

    def test_remove_symbols(self):
        word_token: str = "I_do_not_exist"
        self.assertEqual(
            "Idonotexist",
            self.model.get_instance().remove_symbols(word_token))
        self.assertEqual(
            "name", self.model.get_instance().remove_symbols("##name"))
