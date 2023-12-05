import unittest

from RLEnvForApp.adapter.repository.targetPage.InMemoryTargetPageRepository import InMemoryTargetPageRepository
from RLEnvForApp.usecase.environment.autOperator.dto.CodeCoverageDTO import CodeCoverageDTO
from RLEnvForApp.usecase.targetPage.create import *
from RLEnvForApp.usecase.targetPage.dto.AppEventDTO import AppEventDTO
from RLEnvForApp.usecase.targetPage.dto.DirectiveDTO import DirectiveDTO
from RLEnvForApp.usecase.targetPage.get import *


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self._repository = InMemoryTargetPageRepository()
        self._targetPageUrl = "./register.html"
        self._rootUrl = "./"
        self._taskID = "testTaskID"
        self._appEventDTO = AppEventDTO(xpath="/HTML[1]/BODY[1]/DIV[1]/FORM[1]/DIV[4]/DIV[2]/P[1]/A[2]", value="")
        self._originalCodeCoverageDTO = CodeCoverageDTO(codeCoverageType="statement", codeCoverageVector=[1, 0, 1, 0, 1, 0, 1, 0, 1, 0])
        codeCoverageDTO = CodeCoverageDTO(codeCoverageType="statement", codeCoverageVector=[1, 1, 1, 1, 1, 0, 0, 0, 0, 0])
        self._directiveDTO = DirectiveDTO(appEventDTOs=[self._appEventDTO], codeCoverageDTOs=[codeCoverageDTO])

        createTargetPageUseCase = CreateTargetPageUseCase.CreateTargetPageUseCase(repository=self._repository)
        createTargetPageInput = CreateTargetPageInput.CreateTargetPageInput(targetPageUrl=self._targetPageUrl,
                                                                            rootUrl=self._rootUrl,
                                                                            appEventDTOs=[self._appEventDTO],
                                                                            taskID=self._taskID,
                                                                            basicCodeCoverage=self._originalCodeCoverageDTO,
                                                                            directiveDTOs=[self._directiveDTO])
        createTargetPageOutput = CreateTargetPageOutput.CreateTargetPageOutput()
        createTargetPageUseCase.execute(createTargetPageInput, createTargetPageOutput)
        self._targetPageId = createTargetPageOutput.getId()
    def test_get_all_target_page(self):
        getAllTargetPageUseCase = GetAllTargetPageUseCase.GetAllTargetPageUseCase(repository=self._repository)
        getAllTargetPageInput = GetAllTargetPageInput.GetAllTargetPageInput()
        getAllTargetPageOutput = GetAllTargetPageOutput.GetAllTargetPageOutput()

        getAllTargetPageUseCase.execute(input=getAllTargetPageInput, output=getAllTargetPageOutput)

        self.assertEqual(1, len(getAllTargetPageOutput.getTargetPageDTOs()))