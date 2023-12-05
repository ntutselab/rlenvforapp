import unittest

from RLEnvForApp.adapter.repository.targetPage.InMemoryTargetPageRepository import InMemoryTargetPageRepository
from RLEnvForApp.domain.targetPage.Directive import Directive
from RLEnvForApp.usecase.environment.autOperator.dto.CodeCoverageDTO import CodeCoverageDTO
from RLEnvForApp.usecase.targetPage.dto import AppEventDTO
from RLEnvForApp.usecase.targetPage.create import *
from RLEnvForApp.usecase.targetPage.dto.DirectiveDTO import DirectiveDTO
from RLEnvForApp.usecase.targetPage.entity.TargetPageEntity import TargetPageEntity
from RLEnvForApp.usecase.targetPage.mapper import TargetPageEntityMapper


class testCreateTargetPageUseCase(unittest.TestCase):
    def setUp(self) -> None:
        self._repository = InMemoryTargetPageRepository()

    def test_create_target_page(self):
        targetPageUrl = "./register.html"
        rootUrl = "./"
        createTargetPageUseCase = CreateTargetPageUseCase.CreateTargetPageUseCase(repository=self._repository)
        createTargetPageInput = CreateTargetPageInput.CreateTargetPageInput(targetPageUrl=targetPageUrl, rootUrl=rootUrl, appEventDTOs=[])
        createTargetPageOutput = CreateTargetPageOutput.CreateTargetPageOutput()
        createTargetPageUseCase.execute(createTargetPageInput, createTargetPageOutput)

        targetPageEntity: TargetPageEntity = self._repository.findById(createTargetPageOutput.getId())
        targetPage = TargetPageEntityMapper.mappingTargetPageFrom(targetPageEntity=targetPageEntity)

        self.assertEqual(targetPage.getId(), createTargetPageOutput.getId())

    def test_create_target_page_with_appEvent(self):
        targetPageUrl = "./register.html"
        rootUrl = "./"
        appEventDTO = AppEventDTO.AppEventDTO(xpath="/HTML[1]/BODY[1]/DIV[1]/FORM[1]/DIV[4]/DIV[2]/P[1]/A[2]", value="")

        createTargetPageUseCase = CreateTargetPageUseCase.CreateTargetPageUseCase(repository=self._repository)
        createTargetPageInput = CreateTargetPageInput.CreateTargetPageInput(targetPageUrl=targetPageUrl, rootUrl=rootUrl, appEventDTOs=[appEventDTO])
        createTargetPageOutput = CreateTargetPageOutput.CreateTargetPageOutput()

        createTargetPageUseCase.execute(createTargetPageInput, createTargetPageOutput)

        targetPageEntity: TargetPageEntity = self._repository.findById(createTargetPageOutput.getId())
        targetPage = TargetPageEntityMapper.mappingTargetPageFrom(targetPageEntity=targetPageEntity)
        self.assertEqual(targetPage.getAppEvents()[0].getXpath(), "/HTML[1]/BODY[1]/DIV[1]/FORM[1]/DIV[4]/DIV[2]/P[1]/A[2]")

    def test_create_target_page_for_AIGuide(self):
        targetPageUrl = "./register.html"
        rootUrl = "./"
        appEventDTO = AppEventDTO.AppEventDTO(xpath="/HTML[1]/BODY[1]/DIV[1]/FORM[1]/DIV[4]/DIV[2]/P[1]/A[2]", value="")
        taskID = "testTaskID"
        originalCodeCoverageDTO = CodeCoverageDTO(codeCoverageType="statement", codeCoverageVector=[1, 0, 1, 0, 1, 0, 1, 0, 1, 0])
        codeCoverageDTO = CodeCoverageDTO(codeCoverageType="statement", codeCoverageVector=[1, 1, 1, 1, 1, 0, 0, 0, 0, 0])
        directiveDTO = DirectiveDTO(appEventDTOs=[appEventDTO], codeCoverageDTOs=[codeCoverageDTO])

        createTargetPageUseCase = CreateTargetPageUseCase.CreateTargetPageUseCase(repository=self._repository)
        createTargetPageInput = CreateTargetPageInput.CreateTargetPageInput(targetPageUrl=targetPageUrl,
                                                                            rootUrl=rootUrl,
                                                                            appEventDTOs=[appEventDTO],
                                                                            taskID=taskID,
                                                                            basicCodeCoverage=originalCodeCoverageDTO,
                                                                            directiveDTOs=[directiveDTO])
        createTargetPageOutput = CreateTargetPageOutput.CreateTargetPageOutput()
        createTargetPageUseCase.execute(createTargetPageInput, createTargetPageOutput)

        targetPageEntity: TargetPageEntity = self._repository.findById(createTargetPageOutput.getId())
        self.assertEqual(len(targetPageEntity.getDirectiveEntities()), 1)

        targetPage = TargetPageEntityMapper.mappingTargetPageFrom(targetPageEntity=targetPageEntity)
        self.assertEqual(targetPage.getAppEvents()[0].getXpath(), "/HTML[1]/BODY[1]/DIV[1]/FORM[1]/DIV[4]/DIV[2]/P[1]/A[2]")
        self.assertEqual(targetPage.getRootUrl(), rootUrl)
        self.assertEqual(targetPage.getTargetUrl(), targetPageUrl)
        self.assertEqual(targetPage.getTaskID(), taskID)
        self.assertEqual(targetPage.getBasicCodeCoverageDTO().getCodeCoverageVector(), [1, 0, 1, 0, 1, 0, 1, 0, 1, 0])
        self.assertEqual(len(targetPage.getDirectives()), 1)
        directive: Directive = targetPage.getDirectives()[0]
        self.assertEqual(directive.getCodeCoverages()[0].getCodeCoverageType(), directiveDTO.getCodeCoverageDTOs()[0].getCodeCoverageType())
        self.assertEqual(directive.getCodeCoverages()[0].getCodeCoverageVector(), directiveDTO.getCodeCoverageDTOs()[0].getCodeCoverageVector())
        self.assertEqual(directive.getAppEvents()[0].getXpath(), appEventDTO.getXpath())
        self.assertEqual(directive.getAppEvents()[0].getValue(), appEventDTO.getValue())