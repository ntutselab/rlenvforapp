import unittest

from RLEnvForApp.adapter.repository.targetPage.InMemoryTargetPageRepository import InMemoryTargetPageRepository
from RLEnvForApp.usecase.targetPage.remove import *
from test.usecase.targetPage.TargetPageHierarchyInitial import TargetPageHierarchyInitial


class testRemoveTargetPageUseCase(unittest.TestCase):
    def setUp(self) -> None:
        self._targetPageRepository = InMemoryTargetPageRepository()
        self._targetPageHierarchy = TargetPageHierarchyInitial()

    def test_remove_target_page(self):
        self._targetPageHierarchy.createTargetPage(targetPageRepository=self._targetPageRepository, targetPageUrl="./", rootUrl="", appEventDTOs=[])
        targetPageId = self._targetPageRepository.findAll()[0].getId()

        removeTargetPageUseCase = RemoveTargetPageUseCase.RemoveTargetPageUseCase(repository=self._targetPageRepository)
        removeTargetPageInput = RemoveTargetPageInput.RemoveTargetPageInput(targetPageId=targetPageId)
        removeTargetPageOutput = RemoveTargetPageOutput.RemoveTargetPageOutput()

        removeTargetPageUseCase.execute(input=removeTargetPageInput, output=removeTargetPageOutput)

        self.assertIsNone(self._targetPageRepository.findById(removeTargetPageOutput.getId()))
