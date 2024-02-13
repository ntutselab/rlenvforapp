import unittest

from RLEnvForApp.domain.environment.observationService.converter.ASCIIConverter import \
    ASCIIConverter


class testTimeLogger(unittest.TestCase):
    def set_up(self) -> None:
        pass

    def tear_down(self) -> None:
        pass

    def test_convert(self):
        state_element = ['A', 'S', 'C', 'I', 'I']
        list_dom_feature = ASCIIConverter().convert(state_element=state_element)

        self.assertNotEqual(['A', 'S', 'C', 'I', 'I'], list_dom_feature)
        self.assertEqual([65, 83, 67, 73, 73], list_dom_feature)
