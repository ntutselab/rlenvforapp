import unittest

from RLEnvForApp.domain.environment.observationService.converter.Word2VecSingleton import \
    Word2VecSingleton


class testWord2VecSingleton(unittest.TestCase):
    def setUp(self) -> None:
        self.model = Word2VecSingleton.getInstance()

    def testGetId(self):
        self.assertEqual(
            self.model.getId(),
            Word2VecSingleton.getInstance().getId())

    def testIsInVocab(self):
        word_token: str = "word"
        self.assertTrue(self.model.getInstance().isInVocab(word_token))
        self.assertFalse(self.model.getInstance().isInVocab("I_do_not_exist"))

    def testGetWordVector(self):
        word_token: str = "word"
        self.assertTrue(300, len(self.model.getWordVector(word_token)))

    def testGetWordsVector(self):
        word_tokens: [] = ["word", "sequence"]
        self.assertTrue(300, len(self.model.getWordsVector(word_tokens)))

    def testRemoveSymbols(self):
        word_token: str = "I_do_not_exist"
        self.assertEqual(
            "Idonotexist",
            self.model.getInstance().removeSymbols(word_token))
        self.assertEqual(
            "name", self.model.getInstance().removeSymbols("##name"))
