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


class testUpdateTargetPageUseCase(unittest.TestCase):
    def set_up(self) -> None:
        self._targetPageRepository = InMemoryTargetPageRepository()
        self._targetPageHierarchy = TargetPageHierarchyInitial()

    def test_update_target_url_target_page(self):
        targetPageId = self._targetPageHierarchy.create_target_page(
            targetPageRepository=self._targetPageRepository, targetPageUrl="/", rootUrl="/", appEventDTOs=[])
        input = UpdateTargetPageInput.UpdateTargetPageInput(
            targetPageId=targetPageId, targetPageUrl="/login")
        output = UpdateTargetPageOutput.UpdateTargetPageOutput()
        usecase = UpdateTargetPageUseCase.UpdateTargetPageUseCase(
            repository=self._targetPageRepository)

        usecase.execute(input=input, output=output)
        targetPageEntity = self._targetPageRepository.find_by_id(output.get_id())
        targetPage: TargetPage = TargetPageEntityMapper.mapping_target_page_from(
            targetPageEntity=targetPageEntity)
        self.assertEqual("/login", targetPage.get_target_url())

    def test_update_code_coverage_target_page(self):
        targetPageId = self._targetPageHierarchy.create_target_page(
            targetPageRepository=self._targetPageRepository, targetPageUrl="/", rootUrl="/", appEventDTOs=[])
        input = UpdateTargetPageInput.UpdateTargetPageInput(targetPageId=targetPageId,
                                                            basicCodeCoverageDTO=CodeCoverageDTO(codeCoverageType="test codecoverage",
                                                                                                 codeCoverageVector=[1, 1, 1, 1, 1, 0, 0, 0, 0, 0]))
        output = UpdateTargetPageOutput.UpdateTargetPageOutput()
        usecase = UpdateTargetPageUseCase.UpdateTargetPageUseCase(
            repository=self._targetPageRepository)
        usecase.execute(input=input, output=output)
        targetPageEntity = self._targetPageRepository.find_by_id(output.get_id())
        targetPage: TargetPage = TargetPageEntityMapper.mapping_target_page_from(
            targetPageEntity=targetPageEntity)
        self.assertEqual(
            5, targetPage.get_basic_code_coverage().get_covered_amount())

        input = UpdateTargetPageInput.UpdateTargetPageInput(targetPageId=targetPageId,
                                                            basicCodeCoverageDTO=CodeCoverageDTO(codeCoverageType="test codecoverage",
                                                                                                 codeCoverageVector=[1, 0, 1, 0, 0, 0, 0, 0, 0, 1]))
        output = UpdateTargetPageOutput.UpdateTargetPageOutput()
        usecase = UpdateTargetPageUseCase.UpdateTargetPageUseCase(
            repository=self._targetPageRepository)
        usecase.execute(input=input, output=output)
        targetPageEntity = self._targetPageRepository.find_by_id(output.get_id())
        targetPage: TargetPage = TargetPageEntityMapper.mapping_target_page_from(
            targetPageEntity=targetPageEntity)
        self.assertEqual(
            6, targetPage.get_basic_code_coverage().get_covered_amount())
        self.assertEqual(
            10, targetPage.get_basic_code_coverage().get_code_coverage_vector_length())
