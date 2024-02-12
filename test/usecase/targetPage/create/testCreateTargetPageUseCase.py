import unittest

from RLEnvForApp.adapter.repository.targetPage.InMemoryTargetPageRepository import \
    InMemoryTargetPageRepository
from RLEnvForApp.domain.targetPage.Directive import Directive
from RLEnvForApp.usecase.environment.autOperator.dto.CodeCoverageDTO import \
    CodeCoverageDTO
from RLEnvForApp.usecase.targetPage.create import (CreateTargetPageInput,
                                                   CreateTargetPageOutput,
                                                   CreateTargetPageUseCase)
from RLEnvForApp.usecase.targetPage.dto import AppEventDTO
from RLEnvForApp.usecase.targetPage.dto.DirectiveDTO import DirectiveDTO
from RLEnvForApp.usecase.targetPage.entity.TargetPageEntity import \
    TargetPageEntity
from RLEnvForApp.usecase.targetPage.mapper import TargetPageEntityMapper


class testCreateTargetPageUseCase(unittest.TestCase):
    def set_up(self) -> None:
        self._repository = InMemoryTargetPageRepository()

    def test_create_target_page(self):
        targetPageUrl = "./register.html"
        rootUrl = "./"
        createTargetPageUseCase = CreateTargetPageUseCase.CreateTargetPageUseCase(
            repository=self._repository)
        createTargetPageInput = CreateTargetPageInput.CreateTargetPageInput(
            targetPageUrl=targetPageUrl, rootUrl=rootUrl, appEventDTOs=[])
        createTargetPageOutput = CreateTargetPageOutput.CreateTargetPageOutput()
        createTargetPageUseCase.execute(
            createTargetPageInput, createTargetPageOutput)

        targetPageEntity: TargetPageEntity = self._repository.find_by_id(
            createTargetPageOutput.get_id())
        targetPage = TargetPageEntityMapper.mapping_target_page_from(
            targetPageEntity=targetPageEntity)

        self.assertEqual(targetPage.get_id(), createTargetPageOutput.get_id())

    def test_create_target_page_with_app_event(self):
        targetPageUrl = "./register.html"
        rootUrl = "./"
        appEventDTO = AppEventDTO.AppEventDTO(
            xpath="/HTML[1]/BODY[1]/DIV[1]/FORM[1]/DIV[4]/DIV[2]/P[1]/A[2]", value="")

        createTargetPageUseCase = CreateTargetPageUseCase.CreateTargetPageUseCase(
            repository=self._repository)
        createTargetPageInput = CreateTargetPageInput.CreateTargetPageInput(
            targetPageUrl=targetPageUrl, rootUrl=rootUrl, appEventDTOs=[appEventDTO])
        createTargetPageOutput = CreateTargetPageOutput.CreateTargetPageOutput()

        createTargetPageUseCase.execute(
            createTargetPageInput, createTargetPageOutput)

        targetPageEntity: TargetPageEntity = self._repository.find_by_id(
            createTargetPageOutput.get_id())
        targetPage = TargetPageEntityMapper.mapping_target_page_from(
            targetPageEntity=targetPageEntity)
        self.assertEqual(
            targetPage.get_app_events()[0].get_xpath(),
            "/HTML[1]/BODY[1]/DIV[1]/FORM[1]/DIV[4]/DIV[2]/P[1]/A[2]")

    def test_create_target_page_for_ai_guide(self):
        targetPageUrl = "./register.html"
        rootUrl = "./"
        appEventDTO = AppEventDTO.AppEventDTO(
            xpath="/HTML[1]/BODY[1]/DIV[1]/FORM[1]/DIV[4]/DIV[2]/P[1]/A[2]", value="")
        taskID = "testTaskID"
        originalCodeCoverageDTO = CodeCoverageDTO(
            codeCoverageType="statement", codeCoverageVector=[
                1, 0, 1, 0, 1, 0, 1, 0, 1, 0])
        codeCoverageDTO = CodeCoverageDTO(
            codeCoverageType="statement", codeCoverageVector=[
                1, 1, 1, 1, 1, 0, 0, 0, 0, 0])
        directiveDTO = DirectiveDTO(
            appEventDTOs=[appEventDTO],
            codeCoverageDTOs=[codeCoverageDTO])

        createTargetPageUseCase = CreateTargetPageUseCase.CreateTargetPageUseCase(
            repository=self._repository)
        createTargetPageInput = CreateTargetPageInput.CreateTargetPageInput(targetPageUrl=targetPageUrl,
                                                                            rootUrl=rootUrl,
                                                                            appEventDTOs=[
                                                                                appEventDTO],
                                                                            taskID=taskID,
                                                                            basicCodeCoverage=originalCodeCoverageDTO,
                                                                            directiveDTOs=[directiveDTO])
        createTargetPageOutput = CreateTargetPageOutput.CreateTargetPageOutput()
        createTargetPageUseCase.execute(
            createTargetPageInput, createTargetPageOutput)

        targetPageEntity: TargetPageEntity = self._repository.find_by_id(
            createTargetPageOutput.get_id())
        self.assertEqual(len(targetPageEntity.get_directive_entities()), 1)

        targetPage = TargetPageEntityMapper.mapping_target_page_from(
            targetPageEntity=targetPageEntity)
        self.assertEqual(
            targetPage.get_app_events()[0].get_xpath(),
            "/HTML[1]/BODY[1]/DIV[1]/FORM[1]/DIV[4]/DIV[2]/P[1]/A[2]")
        self.assertEqual(targetPage.get_root_url(), rootUrl)
        self.assertEqual(targetPage.get_target_url(), targetPageUrl)
        self.assertEqual(targetPage.get_task_id(), taskID)
        self.assertEqual(
            targetPage.get_basic_code_coverage_dto().get_code_coverage_vector(), [
                1, 0, 1, 0, 1, 0, 1, 0, 1, 0])
        self.assertEqual(len(targetPage.get_directives()), 1)
        directive: Directive = targetPage.get_directives()[0]
        self.assertEqual(
            directive.get_code_coverages()[0].get_code_coverage_type(),
            directiveDTO.get_code_coverage_dt_os()[0].get_code_coverage_type())
        self.assertEqual(
            directive.get_code_coverages()[0].get_code_coverage_vector(),
            directiveDTO.get_code_coverage_dt_os()[0].get_code_coverage_vector())
        self.assertEqual(
            directive.get_app_events()[0].get_xpath(),
            appEventDTO.get_xpath())
        self.assertEqual(
            directive.get_app_events()[0].get_value(),
            appEventDTO.get_value())
