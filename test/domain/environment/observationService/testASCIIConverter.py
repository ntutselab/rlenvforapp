import unittest

from RLEnvForApp.domain.environment.observationService.converter.ASCIIConverter import \
    ASCIIConverter


class testTimeLogger(unittest.TestCase):
    def set_up(self) -> None:
        pass

    def tear_down(self) -> None:
        pass

    def test_convert(self):
        stateElement = ['A', 'S', 'C', 'I', 'I']
        listDOMFeature = ASCIIConverter().convert(stateElement=stateElement)

        self.assertNotEqual(['A', 'S', 'C', 'I', 'I'], listDOMFeature)
        self.assertEqual([65, 83, 67, 73, 73], listDOMFeature)
