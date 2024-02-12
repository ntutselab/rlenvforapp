import unittest

from RLEnvForApp.adapter.repository.episodeHandler.InMemoryEpisodeHandlerRepository import \
    InMemoryEpisodeHandlerRepository
from RLEnvForApp.adapter.repository.targetPage.InMemoryTargetPageRepository import \
    InMemoryTargetPageRepository
from RLEnvForApp.domain.environment.episodeHandler.MorePagesExperimentEpisodeHandler import \
    MorePagesExperimentEpisodeHandler
from RLEnvForApp.domain.environment.state.AppElement import AppElement
from RLEnvForApp.domain.environment.state.CodeCoverage import CodeCoverage
from RLEnvForApp.domain.environment.state.State import State
from RLEnvForApp.domain.targetPage.DirectiveRuleService.MaxCodeCoverageDirectiveRuleService import \
    MaxCodeCoverageDirectiveRuleService
from RLEnvForApp.usecase.environment.autOperator.dto.CodeCoverageDTO import \
    CodeCoverageDTO
from RLEnvForApp.usecase.environment.episodeHandler.mapper import \
    EpisodeHandlerEntityMapper
from RLEnvForApp.usecase.targetPage.create import (CreateDirectiveInput,
                                                   CreateDirectiveOutput,
                                                   CreateDirectiveUseCase,
                                                   CreateTargetPageInput,
                                                   CreateTargetPageOutput,
                                                   CreateTargetPageUseCase)
from RLEnvForApp.usecase.targetPage.dto.AppEventDTO import AppEventDTO
from RLEnvForApp.usecase.targetPage.mapper import DirectiveDTOMapper


class testCreateDirectiveUseCase(unittest.TestCase):
    def setUp(self) -> None:
        self._codeCoverageType = "statement coverage"
        self._targetPageRepository = InMemoryTargetPageRepository()
        self._episodeHandlerRepository = InMemoryEpisodeHandlerRepository()
        self._targetPageId = self._createTargetPage(repository=self._targetPageRepository)

    def test_no_improved_code_coverage_with_baseline(self):
        episodeHandler = self._createEpisodeHandler()
        episodeHandler.appendState(self._createState(actionType="click",
                                                     interactedElement=self._createAppElement(
                                                         tagName="button", value=""),
                                                     codeCoverages=[self._createCodeCoverage(codeCoverageVector=[1, 0, 0, 0, 0, 0, 0, 0, 0, 0])]))
        self._episodeHandlerRepository.add(
            episodeHandlerEntity=EpisodeHandlerEntityMapper.mappingEpisodeHandlerEntityForm(
                episodeHandler=episodeHandler))

        createDirectiveUseCase = CreateDirectiveUseCase.CreateDirectiveUseCase(targetPageRepository=self._targetPageRepository,
                                                                               episodeHandlerRepository=self._episodeHandlerRepository,
                                                                               directiveRuleService=MaxCodeCoverageDirectiveRuleService())
        createDirectiveInput = CreateDirectiveInput.CreateDirectiveInput(
            targetPageId=self._targetPageId, episodeHandlerId=episodeHandler.getId())
        createDirectiveOutput = CreateDirectiveOutput.CreateDirectiveOutput()

        createDirectiveUseCase.execute(createDirectiveInput, createDirectiveOutput)

        self.assertFalse(createDirectiveOutput.getIsLegalDirective())

    def test_improved_code_coverage_with_baseline_and_more_appEvent(self):
        episodeHandler = self._createEpisodeHandler()
        episodeHandler.appendState(self._createState(actionType="input",
                                                     interactedElement=self._createAppElement(
                                                         tagName="input", value="123"),
                                                     codeCoverages=[self._createCodeCoverage(codeCoverageVector=[0, 1, 0, 0, 0, 0, 0, 0, 0, 0])]))
        episodeHandler.appendState(self._createState(actionType="input",
                                                     interactedElement=self._createAppElement(
                                                         tagName="input", value="456"),
                                                     codeCoverages=[self._createCodeCoverage(codeCoverageVector=[0, 1, 0, 0, 0, 0, 0, 0, 0, 0])]))
        episodeHandler.appendState(self._createState(actionType="click",
                                                     interactedElement=self._createAppElement(
                                                         tagName="button", value=""),
                                                     codeCoverages=[self._createCodeCoverage(codeCoverageVector=[0, 1, 0, 0, 0, 0, 0, 0, 0, 0])]))
        self._episodeHandlerRepository.add(
            episodeHandlerEntity=EpisodeHandlerEntityMapper.mappingEpisodeHandlerEntityForm(
                episodeHandler=episodeHandler))

        createDirectiveUseCase = CreateDirectiveUseCase.CreateDirectiveUseCase(targetPageRepository=self._targetPageRepository,
                                                                               episodeHandlerRepository=self._episodeHandlerRepository,
                                                                               directiveRuleService=MaxCodeCoverageDirectiveRuleService())
        createDirectiveInput = CreateDirectiveInput.CreateDirectiveInput(
            targetPageId=self._targetPageId, episodeHandlerId=episodeHandler.getId())
        createDirectiveOutput = CreateDirectiveOutput.CreateDirectiveOutput()

        createDirectiveUseCase.execute(createDirectiveInput, createDirectiveOutput)

        directiveDTO = createDirectiveOutput.getDirectiveDTO()
        directive = DirectiveDTOMapper.mappingDirectiveFrom(directiveDTO=directiveDTO)
        self.assertTrue(createDirectiveOutput.getIsLegalDirective())
        self.assertEqual(len(directive.getAppEvents()), 3)

    def test_smaller_code_coverage_than_baseline(self):
        episodeHandler = self._createEpisodeHandler()
        episodeHandler.appendState(self._createState(actionType="click",
                                                     interactedElement=self._createAppElement(
                                                         tagName="button", value=""),
                                                     codeCoverages=[self._createCodeCoverage(codeCoverageVector=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0])]))
        self._episodeHandlerRepository.add(
            episodeHandlerEntity=EpisodeHandlerEntityMapper.mappingEpisodeHandlerEntityForm(
                episodeHandler=episodeHandler))

        createDirectiveUseCase = CreateDirectiveUseCase.CreateDirectiveUseCase(targetPageRepository=self._targetPageRepository,
                                                                               episodeHandlerRepository=self._episodeHandlerRepository,
                                                                               directiveRuleService=MaxCodeCoverageDirectiveRuleService())
        createDirectiveInput = CreateDirectiveInput.CreateDirectiveInput(
            targetPageId=self._targetPageId, episodeHandlerId=episodeHandler.getId())
        createDirectiveOutput = CreateDirectiveOutput.CreateDirectiveOutput()

        createDirectiveUseCase.execute(createDirectiveInput, createDirectiveOutput)

        self.assertFalse(createDirectiveOutput.getIsLegalDirective())

    def test_no_improved_code_coverage_with_baseline_and_more_previous_state(self):
        episodeHandler = self._createEpisodeHandler()
        episodeHandler.appendState(self._createState(actionType="click",
                                                     interactedElement=self._createAppElement(
                                                         tagName="button", value=""),
                                                     codeCoverages=[self._createCodeCoverage(codeCoverageVector=[0, 1, 0, 0, 0, 0, 0, 0, 0, 0])]))
        self._episodeHandlerRepository.add(
            episodeHandlerEntity=EpisodeHandlerEntityMapper.mappingEpisodeHandlerEntityForm(
                episodeHandler=episodeHandler))
        self._createDirective(episodeHandlerId=episodeHandler.getId())

        episodeHandler = self._createEpisodeHandler()
        episodeHandler.appendState(self._createState(actionType="click",
                                                     interactedElement=self._createAppElement(
                                                         tagName="button", value=""),
                                                     codeCoverages=[self._createCodeCoverage(codeCoverageVector=[1, 0, 0, 0, 0, 0, 0, 0, 0, 0])]))
        self._episodeHandlerRepository.add(
            episodeHandlerEntity=EpisodeHandlerEntityMapper.mappingEpisodeHandlerEntityForm(
                episodeHandler=episodeHandler))

        createDirectiveUseCase = CreateDirectiveUseCase.CreateDirectiveUseCase(targetPageRepository=self._targetPageRepository,
                                                                               episodeHandlerRepository=self._episodeHandlerRepository,
                                                                               directiveRuleService=MaxCodeCoverageDirectiveRuleService())
        createDirectiveInput = CreateDirectiveInput.CreateDirectiveInput(
            targetPageId=self._targetPageId, episodeHandlerId=episodeHandler.getId())
        createDirectiveOutput = CreateDirectiveOutput.CreateDirectiveOutput()
        createDirectiveUseCase.execute(createDirectiveInput, createDirectiveOutput)
        self.assertFalse(createDirectiveOutput.getIsLegalDirective())

        episodeHandler = self._createEpisodeHandler()
        episodeHandler.appendState(self._createState(actionType="click",
                                                     interactedElement=self._createAppElement(
                                                         tagName="button", value=""),
                                                     codeCoverages=[self._createCodeCoverage(codeCoverageVector=[0, 1, 0, 0, 0, 0, 0, 0, 0, 0])]))
        self._episodeHandlerRepository.add(
            episodeHandlerEntity=EpisodeHandlerEntityMapper.mappingEpisodeHandlerEntityForm(
                episodeHandler=episodeHandler))

        createDirectiveUseCase = CreateDirectiveUseCase.CreateDirectiveUseCase(targetPageRepository=self._targetPageRepository,
                                                                               episodeHandlerRepository=self._episodeHandlerRepository,
                                                                               directiveRuleService=MaxCodeCoverageDirectiveRuleService())
        createDirectiveInput = CreateDirectiveInput.CreateDirectiveInput(
            targetPageId=self._targetPageId, episodeHandlerId=episodeHandler.getId())
        createDirectiveOutput = CreateDirectiveOutput.CreateDirectiveOutput()
        createDirectiveUseCase.execute(createDirectiveInput, createDirectiveOutput)
        self.assertFalse(createDirectiveOutput.getIsLegalDirective())

    def test_smaller_code_coverage_than_baseline_and_previous_state(self):

        episodeHandler = self._createEpisodeHandler()
        episodeHandler.appendState(self._createState(actionType="click",
                                                     interactedElement=self._createAppElement(
                                                         tagName="button", value=""),
                                                     codeCoverages=[self._createCodeCoverage(codeCoverageVector=[0, 1, 0, 0, 0, 0, 0, 0, 0, 0])]))
        self._episodeHandlerRepository.add(
            episodeHandlerEntity=EpisodeHandlerEntityMapper.mappingEpisodeHandlerEntityForm(
                episodeHandler=episodeHandler))
        self._createDirective(episodeHandlerId=episodeHandler.getId())

        episodeHandler = self._createEpisodeHandler()
        episodeHandler.appendState(self._createState(actionType="click",
                                                     interactedElement=self._createAppElement(
                                                         tagName="button", value=""),
                                                     codeCoverages=[self._createCodeCoverage(codeCoverageVector=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0])]))
        self._episodeHandlerRepository.add(
            episodeHandlerEntity=EpisodeHandlerEntityMapper.mappingEpisodeHandlerEntityForm(
                episodeHandler=episodeHandler))

        createDirectiveUseCase = CreateDirectiveUseCase.CreateDirectiveUseCase(targetPageRepository=self._targetPageRepository,
                                                                               episodeHandlerRepository=self._episodeHandlerRepository,
                                                                               directiveRuleService=MaxCodeCoverageDirectiveRuleService())
        createDirectiveInput = CreateDirectiveInput.CreateDirectiveInput(
            targetPageId=self._targetPageId, episodeHandlerId=episodeHandler.getId())
        createDirectiveOutput = CreateDirectiveOutput.CreateDirectiveOutput()

        createDirectiveUseCase.execute(createDirectiveInput, createDirectiveOutput)

        self.assertFalse(createDirectiveOutput.getIsLegalDirective())

    def test_improved_code_coverage_with_baseline_and_with_previous_state(self):
        episodeHandler = self._createEpisodeHandler()
        episodeHandler.appendState(self._createState(actionType="click",
                                                     interactedElement=self._createAppElement(
                                                         tagName="button", value=""),
                                                     codeCoverages=[self._createCodeCoverage(codeCoverageVector=[0, 1, 0, 0, 0, 0, 0, 0, 0, 0])]))
        self._episodeHandlerRepository.add(
            episodeHandlerEntity=EpisodeHandlerEntityMapper.mappingEpisodeHandlerEntityForm(
                episodeHandler=episodeHandler))
        self._createDirective(episodeHandlerId=episodeHandler.getId())

        episodeHandler = self._createEpisodeHandler()
        episodeHandler.appendState(self._createState(actionType="click",
                                                     interactedElement=self._createAppElement(
                                                         tagName="button", value=""),
                                                     codeCoverages=[self._createCodeCoverage(codeCoverageVector=[0, 0, 1, 0, 0, 0, 0, 0, 0, 0])]))
        self._episodeHandlerRepository.add(
            episodeHandlerEntity=EpisodeHandlerEntityMapper.mappingEpisodeHandlerEntityForm(
                episodeHandler=episodeHandler))

        createDirectiveUseCase = CreateDirectiveUseCase.CreateDirectiveUseCase(targetPageRepository=self._targetPageRepository,
                                                                               episodeHandlerRepository=self._episodeHandlerRepository,
                                                                               directiveRuleService=MaxCodeCoverageDirectiveRuleService())
        createDirectiveInput = CreateDirectiveInput.CreateDirectiveInput(
            targetPageId=self._targetPageId, episodeHandlerId=episodeHandler.getId())
        createDirectiveOutput = CreateDirectiveOutput.CreateDirectiveOutput()

        createDirectiveUseCase.execute(createDirectiveInput, createDirectiveOutput)
        self.assertFalse(createDirectiveOutput.getIsLegalDirective())

    def test_same_code_coverage_with_previous_state_but_appEvent_is_smaller(self):
        episodeHandler = self._createEpisodeHandler()
        episodeHandler.appendState(self._createState(actionType="click",
                                                     interactedElement=self._createAppElement(
                                                         tagName="button", value=""),
                                                     codeCoverages=[self._createCodeCoverage(codeCoverageVector=[0, 1, 0, 0, 0, 0, 0, 0, 0, 0])]))
        episodeHandler.appendState(self._createState(actionType="click",
                                                     interactedElement=self._createAppElement(
                                                         tagName="button", value=""),
                                                     codeCoverages=[self._createCodeCoverage(codeCoverageVector=[0, 1, 0, 0, 0, 0, 0, 0, 0, 0])]))
        self._episodeHandlerRepository.add(
            episodeHandlerEntity=EpisodeHandlerEntityMapper.mappingEpisodeHandlerEntityForm(
                episodeHandler=episodeHandler))
        self._createDirective(episodeHandlerId=episodeHandler.getId())

        episodeHandler = self._createEpisodeHandler()
        episodeHandler.appendState(self._createState(actionType="click",
                                                     interactedElement=self._createAppElement(
                                                         tagName="button", value=""),
                                                     codeCoverages=[self._createCodeCoverage(codeCoverageVector=[0, 1, 0, 0, 0, 0, 0, 0, 0, 0])]))
        self._episodeHandlerRepository.add(
            episodeHandlerEntity=EpisodeHandlerEntityMapper.mappingEpisodeHandlerEntityForm(
                episodeHandler=episodeHandler))

        createDirectiveUseCase = CreateDirectiveUseCase.CreateDirectiveUseCase(targetPageRepository=self._targetPageRepository,
                                                                               episodeHandlerRepository=self._episodeHandlerRepository,
                                                                               directiveRuleService=MaxCodeCoverageDirectiveRuleService())
        createDirectiveInput = CreateDirectiveInput.CreateDirectiveInput(
            targetPageId=self._targetPageId, episodeHandlerId=episodeHandler.getId())
        createDirectiveOutput = CreateDirectiveOutput.CreateDirectiveOutput()

        createDirectiveUseCase.execute(createDirectiveInput, createDirectiveOutput)

        directiveDTO = createDirectiveOutput.getDirectiveDTO()
        directive = DirectiveDTOMapper.mappingDirectiveFrom(directiveDTO=directiveDTO)
        self.assertTrue(createDirectiveOutput.getIsLegalDirective())
        self.assertEqual(directive.getAppEvents()[0].getValue(), "")

    def test_same_code_coverage_with_previous_state_but_appEvent_is_bigger(self):
        episodeHandler = self._createEpisodeHandler()
        episodeHandler.appendState(self._createState(actionType="click",
                                                     interactedElement=self._createAppElement(
                                                         tagName="button", value=""),
                                                     codeCoverages=[self._createCodeCoverage(codeCoverageVector=[0, 1, 0, 0, 0, 0, 0, 0, 0, 0])]))
        self._episodeHandlerRepository.add(
            episodeHandlerEntity=EpisodeHandlerEntityMapper.mappingEpisodeHandlerEntityForm(
                episodeHandler=episodeHandler))
        self._createDirective(episodeHandlerId=episodeHandler.getId())

        episodeHandler = self._createEpisodeHandler()
        episodeHandler.appendState(self._createState(actionType="click",
                                                     interactedElement=self._createAppElement(
                                                         tagName="button", value=""),
                                                     codeCoverages=[self._createCodeCoverage(codeCoverageVector=[0, 1, 0, 0, 0, 0, 0, 0, 0, 0])]))
        episodeHandler.appendState(self._createState(actionType="click",
                                                     interactedElement=self._createAppElement(
                                                         tagName="button", value=""),
                                                     codeCoverages=[self._createCodeCoverage(codeCoverageVector=[0, 1, 0, 0, 0, 0, 0, 0, 0, 0])]))
        self._episodeHandlerRepository.add(
            episodeHandlerEntity=EpisodeHandlerEntityMapper.mappingEpisodeHandlerEntityForm(
                episodeHandler=episodeHandler))

        createDirectiveUseCase = CreateDirectiveUseCase.CreateDirectiveUseCase(targetPageRepository=self._targetPageRepository,
                                                                               episodeHandlerRepository=self._episodeHandlerRepository,
                                                                               directiveRuleService=MaxCodeCoverageDirectiveRuleService())
        createDirectiveInput = CreateDirectiveInput.CreateDirectiveInput(
            targetPageId=self._targetPageId, episodeHandlerId=episodeHandler.getId())
        createDirectiveOutput = CreateDirectiveOutput.CreateDirectiveOutput()

        createDirectiveUseCase.execute(createDirectiveInput, createDirectiveOutput)
        self.assertFalse(createDirectiveOutput.getIsLegalDirective())

    def test_smaller_code_coverage_than_previous_state_but_appEvent_is_bigger(self):
        episodeHandler = self._createEpisodeHandler()
        episodeHandler.appendState(self._createState(actionType="click",
                                                     interactedElement=self._createAppElement(
                                                         tagName="button", value=""),
                                                     codeCoverages=[self._createCodeCoverage(codeCoverageVector=[0, 1, 1, 0, 0, 0, 0, 0, 0, 0])]))
        self._episodeHandlerRepository.add(
            episodeHandlerEntity=EpisodeHandlerEntityMapper.mappingEpisodeHandlerEntityForm(
                episodeHandler=episodeHandler))
        self._createDirective(episodeHandlerId=episodeHandler.getId())

        episodeHandler = self._createEpisodeHandler()
        episodeHandler.appendState(self._createState(actionType="click",
                                                     interactedElement=self._createAppElement(
                                                         tagName="button", value=""),
                                                     codeCoverages=[self._createCodeCoverage(codeCoverageVector=[0, 1, 0, 0, 0, 0, 0, 0, 0, 0])]))
        episodeHandler.appendState(self._createState(actionType="click",
                                                     interactedElement=self._createAppElement(
                                                         tagName="button", value=""),
                                                     codeCoverages=[self._createCodeCoverage(codeCoverageVector=[0, 1, 0, 0, 0, 0, 0, 0, 0, 0])]))
        self._episodeHandlerRepository.add(
            episodeHandlerEntity=EpisodeHandlerEntityMapper.mappingEpisodeHandlerEntityForm(
                episodeHandler=episodeHandler))

        createDirectiveUseCase = CreateDirectiveUseCase.CreateDirectiveUseCase(targetPageRepository=self._targetPageRepository,
                                                                               episodeHandlerRepository=self._episodeHandlerRepository,
                                                                               directiveRuleService=MaxCodeCoverageDirectiveRuleService())
        createDirectiveInput = CreateDirectiveInput.CreateDirectiveInput(
            targetPageId=self._targetPageId, episodeHandlerId=episodeHandler.getId())
        createDirectiveOutput = CreateDirectiveOutput.CreateDirectiveOutput()

        createDirectiveUseCase.execute(createDirectiveInput, createDirectiveOutput)
        self.assertFalse(createDirectiveOutput.getIsLegalDirective())

    def test_no_improved_code_coverage_with_previous_state(self):
        episodeHandler = self._createEpisodeHandler()
        episodeHandler.appendState(self._createState(actionType="click",
                                                     interactedElement=self._createAppElement(
                                                         tagName="button", value=""),
                                                     codeCoverages=[self._createCodeCoverage(codeCoverageVector=[0, 1, 0, 0, 0, 0, 0, 0, 0, 0])]))
        self._episodeHandlerRepository.add(
            episodeHandlerEntity=EpisodeHandlerEntityMapper.mappingEpisodeHandlerEntityForm(
                episodeHandler=episodeHandler))
        self._createDirective(episodeHandlerId=episodeHandler.getId())

        episodeHandler = self._createEpisodeHandler()
        episodeHandler.appendState(self._createState(actionType="click",
                                                     interactedElement=self._createAppElement(
                                                         tagName="button", value=""),
                                                     codeCoverages=[self._createCodeCoverage(codeCoverageVector=[0, 1, 0, 0, 0, 0, 0, 0, 0, 0])]))
        self._episodeHandlerRepository.add(
            episodeHandlerEntity=EpisodeHandlerEntityMapper.mappingEpisodeHandlerEntityForm(
                episodeHandler=episodeHandler))

        createDirectiveUseCase = CreateDirectiveUseCase.CreateDirectiveUseCase(targetPageRepository=self._targetPageRepository,
                                                                               episodeHandlerRepository=self._episodeHandlerRepository,
                                                                               directiveRuleService=MaxCodeCoverageDirectiveRuleService())
        createDirectiveInput = CreateDirectiveInput.CreateDirectiveInput(
            targetPageId=self._targetPageId, episodeHandlerId=episodeHandler.getId())
        createDirectiveOutput = CreateDirectiveOutput.CreateDirectiveOutput()

        createDirectiveUseCase.execute(createDirectiveInput, createDirectiveOutput)

        directiveDTO = createDirectiveOutput.getDirectiveDTO()
        directive = DirectiveDTOMapper.mappingDirectiveFrom(directiveDTO=directiveDTO)
        self.assertFalse(createDirectiveOutput.getIsLegalDirective())
        self.assertEqual(directive.getAppEvents()[0].getValue(), "")

    def _createTargetPage(self, repository):
        targetPageUrl = "./register.html"
        rootUrl = "./"
        appEventDTO = AppEventDTO(
            xpath="/HTML[1]/BODY[1]/DIV[1]/FORM[1]/DIV[4]/DIV[2]/P[1]/A[2]", value="")
        taskID = "testTaskID"
        originalCodeCoverageDTO = self._createCodeCoverageDTO(
            codeCoverageVector=[1, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        createTargetPageUseCase = CreateTargetPageUseCase.CreateTargetPageUseCase(
            repository=repository)
        createTargetPageInput = CreateTargetPageInput.CreateTargetPageInput(targetPageUrl=targetPageUrl,
                                                                            rootUrl=rootUrl,
                                                                            appEventDTOs=[
                                                                                appEventDTO],
                                                                            taskID=taskID,
                                                                            basicCodeCoverage=originalCodeCoverageDTO)
        createTargetPageOutput = CreateTargetPageOutput.CreateTargetPageOutput()
        createTargetPageUseCase.execute(createTargetPageInput, createTargetPageOutput)
        return createTargetPageOutput.getId()

    def _createCodeCoverageDTO(self, codeCoverageVector: [bool]) -> CodeCoverageDTO:
        return CodeCoverageDTO(codeCoverageType=self._codeCoverageType,
                               codeCoverageVector=codeCoverageVector)

    def _createCodeCoverage(self, codeCoverageVector: [bool]) -> CodeCoverage:
        return CodeCoverage(codeCoverageType=self._codeCoverageType,
                            codeCoverageVector=codeCoverageVector)

    def _createEpisodeHandler(self):
        return MorePagesExperimentEpisodeHandler(
            id="episodeHandlerId", episodeIndex=0, episodeStep=16)

    def _createState(self, actionType: str, interactedElement: AppElement,
                     codeCoverages: [CodeCoverage]) -> State:
        state = State(id="stateId")
        state.setActionType(actionType=actionType)
        state.setInteractedElement(interactedElement=interactedElement)
        state.setCodeCoverages(codeCoverages=codeCoverages)
        return state

    def _createAppElement(self, tagName: str, value: str):
        return AppElement(tagName=tagName, name="", type="", value=value, xpath="")

    def _createDirective(self, episodeHandlerId: str):
        createDirectiveUseCase = CreateDirectiveUseCase.CreateDirectiveUseCase(targetPageRepository=self._targetPageRepository,
                                                                               episodeHandlerRepository=self._episodeHandlerRepository,
                                                                               directiveRuleService=MaxCodeCoverageDirectiveRuleService())
        createDirectiveInput = CreateDirectiveInput.CreateDirectiveInput(
            targetPageId=self._targetPageId, episodeHandlerId=episodeHandlerId)
        createDirectiveOutput = CreateDirectiveOutput.CreateDirectiveOutput()
        createDirectiveUseCase.execute(createDirectiveInput, createDirectiveOutput)
