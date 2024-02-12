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
    def setUp(self) -> None:
        self._targetPageRepository = InMemoryTargetPageRepository()
        self._targetPageHierarchy = TargetPageHierarchyInitial()

    def test_update_targetUrl_targetPage(self):
        targetPageId = self._targetPageHierarchy.createTargetPage(
            targetPageRepository=self._targetPageRepository, targetPageUrl="/", rootUrl="/", appEventDTOs=[])
        input = UpdateTargetPageInput.UpdateTargetPageInput(
            targetPageId=targetPageId, targetPageUrl="/login")
        output = UpdateTargetPageOutput.UpdateTargetPageOutput()
        usecase = UpdateTargetPageUseCase.UpdateTargetPageUseCase(
            repository=self._targetPageRepository)

        usecase.execute(input=input, output=output)
        targetPageEntity = self._targetPageRepository.findById(output.getId())
        targetPage: TargetPage = TargetPageEntityMapper.mappingTargetPageFrom(
            targetPageEntity=targetPageEntity)
        self.assertEqual("/login", targetPage.getTargetUrl())

    def test_update_codeCoverage_targetPage(self):
        targetPageId = self._targetPageHierarchy.createTargetPage(
            targetPageRepository=self._targetPageRepository, targetPageUrl="/", rootUrl="/", appEventDTOs=[])
        input = UpdateTargetPageInput.UpdateTargetPageInput(targetPageId=targetPageId,
                                                            basicCodeCoverageDTO=CodeCoverageDTO(codeCoverageType="test codecoverage",
                                                                                                 codeCoverageVector=[1, 1, 1, 1, 1, 0, 0, 0, 0, 0]))
        output = UpdateTargetPageOutput.UpdateTargetPageOutput()
        usecase = UpdateTargetPageUseCase.UpdateTargetPageUseCase(
            repository=self._targetPageRepository)
        usecase.execute(input=input, output=output)
        targetPageEntity = self._targetPageRepository.findById(output.getId())
        targetPage: TargetPage = TargetPageEntityMapper.mappingTargetPageFrom(
            targetPageEntity=targetPageEntity)
        self.assertEqual(5, targetPage.getBasicCodeCoverage().getCoveredAmount())

        input = UpdateTargetPageInput.UpdateTargetPageInput(targetPageId=targetPageId,
                                                            basicCodeCoverageDTO=CodeCoverageDTO(codeCoverageType="test codecoverage",
                                                                                                 codeCoverageVector=[1, 0, 1, 0, 0, 0, 0, 0, 0, 1]))
        output = UpdateTargetPageOutput.UpdateTargetPageOutput()
        usecase = UpdateTargetPageUseCase.UpdateTargetPageUseCase(
            repository=self._targetPageRepository)
        usecase.execute(input=input, output=output)
        targetPageEntity = self._targetPageRepository.findById(output.getId())
        targetPage: TargetPage = TargetPageEntityMapper.mappingTargetPageFrom(
            targetPageEntity=targetPageEntity)
        self.assertEqual(6, targetPage.getBasicCodeCoverage().getCoveredAmount())
        self.assertEqual(10, targetPage.getBasicCodeCoverage().getCodeCoverageVectorLength())
