import unittest

from RLEnvForApp.adapter.repository.targetPage.InMemoryTargetPageRepository import InMemoryTargetPageRepository
from RLEnvForApp.usecase.environment.autOperator.dto.CodeCoverageDTO import CodeCoverageDTO
from RLEnvForApp.usecase.targetPage.create import CreateTargetPageUseCase, CreateTargetPageInput, CreateTargetPageOutput
from RLEnvForApp.usecase.targetPage.dto.AppEventDTO import AppEventDTO
from RLEnvForApp.usecase.targetPage.dto.DirectiveDTO import DirectiveDTO
from RLEnvForApp.usecase.targetPage.dto.TargetPageDTO import TargetPageDTO
from RLEnvForApp.usecase.targetPage.get import GetTargetPageUseCase, GetTargetPageInput, GetTargetPageOutput


class testGetTargetPageUsecase(unittest.TestCase):
    def setUp(self) -> None:
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
        createTargetPageUseCase.execute(createTargetPageInput, createTargetPageOutput)
        self._targetPageId = createTargetPageOutput.getId()

    def test_get_target_page(self):
        getTargetPageUseCase = GetTargetPageUseCase.GetTargetPageUseCase(
            repository=self._repository)
        getTargetPageInput = GetTargetPageInput.GetTargetPageInput(targetPageId=self._targetPageId)
        getTargetPageOutput = GetTargetPageOutput.GetTargetPageOutput()

        getTargetPageUseCase.execute(input=getTargetPageInput, output=getTargetPageOutput)
        targetPageDTO: TargetPageDTO = getTargetPageOutput.getTargetPageDTO()
        self.assertEqual(targetPageDTO.getId(), self._targetPageId)
        self.assertEqual(
            targetPageDTO.getAppEventDTOs()[0].getXpath(),
            "/HTML[1]/BODY[1]/DIV[1]/FORM[1]/DIV[4]/DIV[2]/P[1]/A[2]")
        self.assertEqual(targetPageDTO.getRootUrl(), self._rootUrl)
        self.assertEqual(targetPageDTO.getTargetUrl(), self._targetPageUrl)
        self.assertEqual(targetPageDTO.getTaskID(), self._taskID)
        self.assertEqual(
            targetPageDTO.getBasicCodeCoverageDTO().getCodeCoverageVector(), [
                1, 0, 1, 0, 1, 0, 1, 0, 1, 0])
        self.assertEqual(len(targetPageDTO.getDirectiveDTOs()), 1)

        directiveDTO: DirectiveDTO = targetPageDTO.getDirectiveDTOs()[0]
        self.assertEqual(directiveDTO.getCodeCoverageDTO().getCodeCoverageType(),
                         self._directiveDTO.getCodeCoverageDTO().getCodeCoverageType())
        self.assertEqual(directiveDTO.getCodeCoverageDTO().getCodeCoverageVector(),
                         self._directiveDTO.getCodeCoverageDTO().getCodeCoverageVector())
        self.assertEqual(directiveDTO.getAppEventDTOs()[0].getXpath(), self._appEventDTO.getXpath())
        self.assertEqual(directiveDTO.getAppEventDTOs()[0].getValue(), self._appEventDTO.getValue())
