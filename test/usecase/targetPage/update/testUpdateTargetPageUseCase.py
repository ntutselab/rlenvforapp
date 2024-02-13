import unittest
from test.usecase.targetPage.TargetPageHierarchyInitial import \
    TargetPageHierarchyInitial

from RLEnvForApp.adapter.repository.targetPage.InMemoryTargetPageRepository import \
    InMemoryTargetPageRepository
from RLEnvForApp.domain.targetPage.TargetPage import TargetPage
from RLEnvForApp.usecase.environment.autOperator.dto.CodeCoverageDTO import \
    CodeCoverageDTO
from RLEnvForApp.usecase.targetPage.mapper import TargetPageEntityMapper
from RLEnvForApp.usecase.targetPage.update import (UpdateTargetPageInput,
                                                   UpdateTargetPageOutput,
                                                   UpdateTargetPageUseCase)


class TestUpdateTargetPageUseCase(unittest.TestCase):
    def set_up(self) -> None:
        self._target_page_repository = InMemoryTargetPageRepository()
        self._target_page_hierarchy = TargetPageHierarchyInitial()

    def test_update_target_url_target_page(self):
        target_page_id = self._target_page_hierarchy.create_target_page(
            targetPageRepository=self._target_page_repository, target_page_url="/", root_url="/", app_event_dt_os=[])
        input = UpdateTargetPageInput.UpdateTargetPageInput(
            target_page_id=target_page_id, target_page_url="/login")
        output = UpdateTargetPageOutput.UpdateTargetPageOutput()
        usecase = UpdateTargetPageUseCase.UpdateTargetPageUseCase(
            repository=self._target_page_repository)

        usecase.execute(input=input, output=output)
        target_page_entity = self._target_page_repository.find_by_id(output.get_id())
        target_page: TargetPage = TargetPageEntityMapper.mapping_target_page_from(
            target_page_entity=target_page_entity)
        self.assertEqual("/login", target_page.get_target_url())

    def test_update_code_coverage_target_page(self):
        target_page_id = self._target_page_hierarchy.create_target_page(
            targetPageRepository=self._target_page_repository, target_page_url="/", root_url="/", app_event_dt_os=[])
        input = UpdateTargetPageInput.UpdateTargetPageInput(target_page_id=target_page_id,
                                                            basic_code_coverage_dto=CodeCoverageDTO(code_coverage_type="test codecoverage",
                                                                                                 code_coverage_vector=[1, 1, 1, 1, 1, 0, 0, 0, 0, 0]))
        output = UpdateTargetPageOutput.UpdateTargetPageOutput()
        usecase = UpdateTargetPageUseCase.UpdateTargetPageUseCase(
            repository=self._target_page_repository)
        usecase.execute(input=input, output=output)
        target_page_entity = self._target_page_repository.find_by_id(output.get_id())
        target_page: TargetPage = TargetPageEntityMapper.mapping_target_page_from(
            target_page_entity=target_page_entity)
        self.assertEqual(
            5, target_page.get_basic_code_coverage().get_covered_amount())

        input = UpdateTargetPageInput.UpdateTargetPageInput(target_page_id=target_page_id,
                                                            basic_code_coverage_dto=CodeCoverageDTO(code_coverage_type="test codecoverage",
                                                                                                 code_coverage_vector=[1, 0, 1, 0, 0, 0, 0, 0, 0, 1]))
        output = UpdateTargetPageOutput.UpdateTargetPageOutput()
        usecase = UpdateTargetPageUseCase.UpdateTargetPageUseCase(
            repository=self._target_page_repository)
        usecase.execute(input=input, output=output)
        target_page_entity = self._target_page_repository.find_by_id(output.get_id())
        target_page: TargetPage = TargetPageEntityMapper.mapping_target_page_from(
            target_page_entity=target_page_entity)
        self.assertEqual(
            6, target_page.get_basic_code_coverage().get_covered_amount())
        self.assertEqual(
            10, target_page.get_basic_code_coverage().get_code_coverage_vector_length())
