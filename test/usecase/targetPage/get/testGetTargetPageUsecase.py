import unittest

from RLEnvForApp.adapter.repository.targetPage.InMemoryTargetPageRepository import \
    InMemoryTargetPageRepository
from RLEnvForApp.usecase.environment.autOperator.dto.CodeCoverageDTO import \
    CodeCoverageDTO
from RLEnvForApp.usecase.targetPage.create import (CreateTargetPageInput,
                                                   CreateTargetPageOutput,
                                                   CreateTargetPageUseCase)
from RLEnvForApp.usecase.targetPage.dto.AppEventDTO import AppEventDTO
from RLEnvForApp.usecase.targetPage.dto.DirectiveDTO import DirectiveDTO
from RLEnvForApp.usecase.targetPage.dto.TargetPageDTO import TargetPageDTO
from RLEnvForApp.usecase.targetPage.get import (GetTargetPageInput,
                                                GetTargetPageOutput,
                                                GetTargetPageUseCase)


class testGetTargetPageUsecase(unittest.TestCase):
    def set_up(self) -> None:
        self._repository = InMemoryTargetPageRepository()
        self._targetPageUrl = "./register.html"
        self._rootUrl = "./"
        self._taskID = "testTaskID"
        self._appEventDTO = AppEventDTO(
            xpath="/HTML[1]/BODY[1]/DIV[1]/FORM[1]/DIV[4]/DIV[2]/P[1]/A[2]", value="")
        self._originalCodeCoverageDTO = CodeCoverageDTO(
            codeCoverageType="statement", codeCoverageVector=[
                1, 0, 1, 0, 1, 0, 1, 0, 1, 0])
        codeCoverageDTO = CodeCoverageDTO(
            codeCoverageType="statement", codeCoverageVector=[
                1, 1, 1, 1, 1, 0, 0, 0, 0, 0])
        self._directiveDTO = DirectiveDTO(
            appEventDTOs=[
                self._appEventDTO],
            codeCoverageDTO=codeCoverageDTO)

        createTargetPageUseCase = CreateTargetPageUseCase.CreateTargetPageUseCase(
            repository=self._repository)
        createTargetPageInput = CreateTargetPageInput.CreateTargetPageInput(targetPageUrl=self._targetPageUrl,
                                                                            rootUrl=self._rootUrl,
                                                                            appEventDTOs=[
                                                                                self._appEventDTO],
                                                                            taskID=self._taskID,
                                                                            basicCodeCoverage=self._originalCodeCoverageDTO,
                                                                            directiveDTOs=[self._directiveDTO])
        createTargetPageOutput = CreateTargetPageOutput.CreateTargetPageOutput()
        createTargetPageUseCase.execute(
            createTargetPageInput, createTargetPageOutput)
        self._targetPageId = createTargetPageOutput.get_id()

    def test_get_target_page(self):
        getTargetPageUseCase = GetTargetPageUseCase.GetTargetPageUseCase(
            repository=self._repository)
        getTargetPageInput = GetTargetPageInput.GetTargetPageInput(
            targetPageId=self._targetPageId)
        getTargetPageOutput = GetTargetPageOutput.GetTargetPageOutput()

        getTargetPageUseCase.execute(
            input=getTargetPageInput,
            output=getTargetPageOutput)
        targetPageDTO: TargetPageDTO = getTargetPageOutput.get_target_page_dto()
        self.assertEqual(targetPageDTO.get_id(), self._targetPageId)
        self.assertEqual(
            targetPageDTO.get_app_event_dt_os()[0].get_xpath(),
            "/HTML[1]/BODY[1]/DIV[1]/FORM[1]/DIV[4]/DIV[2]/P[1]/A[2]")
        self.assertEqual(targetPageDTO.get_root_url(), self._rootUrl)
        self.assertEqual(targetPageDTO.get_target_url(), self._targetPageUrl)
        self.assertEqual(targetPageDTO.get_task_id(), self._taskID)
        self.assertEqual(
            targetPageDTO.get_basic_code_coverage_dto().get_code_coverage_vector(), [
                1, 0, 1, 0, 1, 0, 1, 0, 1, 0])
        self.assertEqual(len(targetPageDTO.get_directive_dt_os()), 1)

        directiveDTO: DirectiveDTO = targetPageDTO.get_directive_dt_os()[0]
        self.assertEqual(directiveDTO.getCodeCoverageDTO().get_code_coverage_type(),
                         self._directiveDTO.getCodeCoverageDTO().get_code_coverage_type())
        self.assertEqual(directiveDTO.getCodeCoverageDTO().get_code_coverage_vector(),
                         self._directiveDTO.getCodeCoverageDTO().get_code_coverage_vector())
        self.assertEqual(
            directiveDTO.get_app_event_dt_os()[0].get_xpath(),
            self._appEventDTO.get_xpath())
        self.assertEqual(
            directiveDTO.get_app_event_dt_os()[0].get_value(),
            self._appEventDTO.get_value())
