import unittest

from RLEnvForApp.domain.environment.observationService.converter.FastTextSingleton import \
    FastTextSingleton


class testFastTextSingleton(unittest.TestCase):
    def setUp(self) -> None:
        self.model = FastTextSingleton.getInstance()

    def testGetId(self):
        self.assertEqual(self.model.getId(), FastTextSingleton.getInstance().getId())

    def testGetWordVector(self):
        word_token: str = "word"
        self.assertTrue(300, len(self.model.getWordVector(word_token)))

    def testGetWordsVector(self):
        word_tokens: [] = ["word", "sequence"]
        self.assertTrue(300, len(self.model.getWordsVector(word_tokens)))
