import unittest
from test.usecase.targetPage.TargetPageHierarchyInitial import \
    TargetPageHierarchyInitial

from RLEnvForApp.adapter.repository.targetPage.InMemoryTargetPageRepository import \
    InMemoryTargetPageRepository
from RLEnvForApp.usecase.targetPage.remove import (RemoveTargetPageInput,
                                                   RemoveTargetPageOutput,
                                                   RemoveTargetPageUseCase)


class TestRemoveTargetPageUseCase(unittest.TestCase):
    def set_up(self) -> None:
        self._target_page_repository = InMemoryTargetPageRepository()
        self._target_page_hierarchy = TargetPageHierarchyInitial()

    def test_remove_target_page(self):
        self._target_page_hierarchy.create_target_page(
            targetPageRepository=self._target_page_repository,
            target_page_url="./",
            root_url="",
            app_event_dt_os=[])
        target_page_id = self._target_page_repository.find_all()[0].get_id()

        remove_target_page_use_case = RemoveTargetPageUseCase.RemoveTargetPageUseCase(
            repository=self._target_page_repository)
        remove_target_page_input = RemoveTargetPageInput.RemoveTargetPageInput(
            target_page_id=target_page_id)
        remove_target_page_output = RemoveTargetPageOutput.RemoveTargetPageOutput()

        remove_target_page_use_case.execute(
            input=remove_target_page_input,
            output=remove_target_page_output)

        self.assertIsNone(
            self._target_page_repository.find_by_id(
                remove_target_page_output.get_id()))
