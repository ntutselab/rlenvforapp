import unittest
from test.usecase.targetPage.TargetPageHierarchyInitial import \
    TargetPageHierarchyInitial

from RLEnvForApp.adapter.repository.targetPage.InMemoryTargetPageRepository import \
    InMemoryTargetPageRepository
from RLEnvForApp.usecase.targetPage.remove import (RemoveTargetPageInput,
                                                   RemoveTargetPageOutput,
                                                   RemoveTargetPageUseCase)


class testRemoveTargetPageUseCase(unittest.TestCase):
    def set_up(self) -> None:
        self._targetPageRepository = InMemoryTargetPageRepository()
        self._targetPageHierarchy = TargetPageHierarchyInitial()

    def test_remove_target_page(self):
        self._targetPageHierarchy.create_target_page(
            targetPageRepository=self._targetPageRepository,
            targetPageUrl="./",
            rootUrl="",
            appEventDTOs=[])
        targetPageId = self._targetPageRepository.find_all()[0].get_id()

        removeTargetPageUseCase = RemoveTargetPageUseCase.RemoveTargetPageUseCase(
            repository=self._targetPageRepository)
        removeTargetPageInput = RemoveTargetPageInput.RemoveTargetPageInput(
            targetPageId=targetPageId)
        removeTargetPageOutput = RemoveTargetPageOutput.RemoveTargetPageOutput()

        removeTargetPageUseCase.execute(
            input=removeTargetPageInput,
            output=removeTargetPageOutput)

        self.assertIsNone(
            self._targetPageRepository.find_by_id(
                removeTargetPageOutput.get_id()))
