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
    def set_up(self) -> None:
        self._codeCoverageType = "statement coverage"
        self._targetPageRepository = InMemoryTargetPageRepository()
        self._episodeHandlerRepository = InMemoryEpisodeHandlerRepository()
        self._targetPageId = self._create_target_page(
            repository=self._targetPageRepository)

    def test_no_improved_code_coverage_with_baseline(self):
        episodeHandler = self._create_episode_handler()
        episodeHandler.append_state(self._create_state(actionType="click",
                                                     interactedElement=self._create_app_element(
                                                         tagName="button", value=""),
                                                     codeCoverages=[self._create_code_coverage(codeCoverageVector=[1, 0, 0, 0, 0, 0, 0, 0, 0, 0])]))
        self._episodeHandlerRepository.add(
            episodeHandlerEntity=EpisodeHandlerEntityMapper.mapping_episode_handler_entity_form(
                episodeHandler=episodeHandler))

        createDirectiveUseCase = CreateDirectiveUseCase.CreateDirectiveUseCase(targetPageRepository=self._targetPageRepository,
                                                                               episodeHandlerRepository=self._episodeHandlerRepository,
                                                                               directiveRuleService=MaxCodeCoverageDirectiveRuleService())
        createDirectiveInput = CreateDirectiveInput.CreateDirectiveInput(
            targetPageId=self._targetPageId, episodeHandlerId=episodeHandler.get_id())
        createDirectiveOutput = CreateDirectiveOutput.CreateDirectiveOutput()

        createDirectiveUseCase.execute(
            createDirectiveInput, createDirectiveOutput)

        self.assertFalse(createDirectiveOutput.get_is_legal_directive())

    def test_improved_code_coverage_with_baseline_and_more_app_event(self):
        episodeHandler = self._create_episode_handler()
        episodeHandler.append_state(self._create_state(actionType="input",
                                                     interactedElement=self._create_app_element(
                                                         tagName="input", value="123"),
                                                     codeCoverages=[self._create_code_coverage(codeCoverageVector=[0, 1, 0, 0, 0, 0, 0, 0, 0, 0])]))
        episodeHandler.append_state(self._create_state(actionType="input",
                                                     interactedElement=self._create_app_element(
                                                         tagName="input", value="456"),
                                                     codeCoverages=[self._create_code_coverage(codeCoverageVector=[0, 1, 0, 0, 0, 0, 0, 0, 0, 0])]))
        episodeHandler.append_state(self._create_state(actionType="click",
                                                     interactedElement=self._create_app_element(
                                                         tagName="button", value=""),
                                                     codeCoverages=[self._create_code_coverage(codeCoverageVector=[0, 1, 0, 0, 0, 0, 0, 0, 0, 0])]))
        self._episodeHandlerRepository.add(
            episodeHandlerEntity=EpisodeHandlerEntityMapper.mapping_episode_handler_entity_form(
                episodeHandler=episodeHandler))

        createDirectiveUseCase = CreateDirectiveUseCase.CreateDirectiveUseCase(targetPageRepository=self._targetPageRepository,
                                                                               episodeHandlerRepository=self._episodeHandlerRepository,
                                                                               directiveRuleService=MaxCodeCoverageDirectiveRuleService())
        createDirectiveInput = CreateDirectiveInput.CreateDirectiveInput(
            targetPageId=self._targetPageId, episodeHandlerId=episodeHandler.get_id())
        createDirectiveOutput = CreateDirectiveOutput.CreateDirectiveOutput()

        createDirectiveUseCase.execute(
            createDirectiveInput, createDirectiveOutput)

        directiveDTO = createDirectiveOutput.get_directive_dto()
        directive = DirectiveDTOMapper.mapping_directive_from(
            directiveDTO=directiveDTO)
        self.assertTrue(createDirectiveOutput.get_is_legal_directive())
        self.assertEqual(len(directive.get_app_events()), 3)

    def test_smaller_code_coverage_than_baseline(self):
        episodeHandler = self._create_episode_handler()
        episodeHandler.append_state(self._create_state(actionType="click",
                                                     interactedElement=self._create_app_element(
                                                         tagName="button", value=""),
                                                     codeCoverages=[self._create_code_coverage(codeCoverageVector=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0])]))
        self._episodeHandlerRepository.add(
            episodeHandlerEntity=EpisodeHandlerEntityMapper.mapping_episode_handler_entity_form(
                episodeHandler=episodeHandler))

        createDirectiveUseCase = CreateDirectiveUseCase.CreateDirectiveUseCase(targetPageRepository=self._targetPageRepository,
                                                                               episodeHandlerRepository=self._episodeHandlerRepository,
                                                                               directiveRuleService=MaxCodeCoverageDirectiveRuleService())
        createDirectiveInput = CreateDirectiveInput.CreateDirectiveInput(
            targetPageId=self._targetPageId, episodeHandlerId=episodeHandler.get_id())
        createDirectiveOutput = CreateDirectiveOutput.CreateDirectiveOutput()

        createDirectiveUseCase.execute(
            createDirectiveInput, createDirectiveOutput)

        self.assertFalse(createDirectiveOutput.get_is_legal_directive())

    def test_no_improved_code_coverage_with_baseline_and_more_previous_state(
            self):
        episodeHandler = self._create_episode_handler()
        episodeHandler.append_state(self._create_state(actionType="click",
                                                     interactedElement=self._create_app_element(
                                                         tagName="button", value=""),
                                                     codeCoverages=[self._create_code_coverage(codeCoverageVector=[0, 1, 0, 0, 0, 0, 0, 0, 0, 0])]))
        self._episodeHandlerRepository.add(
            episodeHandlerEntity=EpisodeHandlerEntityMapper.mapping_episode_handler_entity_form(
                episodeHandler=episodeHandler))
        self._create_directive(episodeHandlerId=episodeHandler.get_id())

        episodeHandler = self._create_episode_handler()
        episodeHandler.append_state(self._create_state(actionType="click",
                                                     interactedElement=self._create_app_element(
                                                         tagName="button", value=""),
                                                     codeCoverages=[self._create_code_coverage(codeCoverageVector=[1, 0, 0, 0, 0, 0, 0, 0, 0, 0])]))
        self._episodeHandlerRepository.add(
            episodeHandlerEntity=EpisodeHandlerEntityMapper.mapping_episode_handler_entity_form(
                episodeHandler=episodeHandler))

        createDirectiveUseCase = CreateDirectiveUseCase.CreateDirectiveUseCase(targetPageRepository=self._targetPageRepository,
                                                                               episodeHandlerRepository=self._episodeHandlerRepository,
                                                                               directiveRuleService=MaxCodeCoverageDirectiveRuleService())
        createDirectiveInput = CreateDirectiveInput.CreateDirectiveInput(
            targetPageId=self._targetPageId, episodeHandlerId=episodeHandler.get_id())
        createDirectiveOutput = CreateDirectiveOutput.CreateDirectiveOutput()
        createDirectiveUseCase.execute(
            createDirectiveInput, createDirectiveOutput)
        self.assertFalse(createDirectiveOutput.get_is_legal_directive())

        episodeHandler = self._create_episode_handler()
        episodeHandler.append_state(self._create_state(actionType="click",
                                                     interactedElement=self._create_app_element(
                                                         tagName="button", value=""),
                                                     codeCoverages=[self._create_code_coverage(codeCoverageVector=[0, 1, 0, 0, 0, 0, 0, 0, 0, 0])]))
        self._episodeHandlerRepository.add(
            episodeHandlerEntity=EpisodeHandlerEntityMapper.mapping_episode_handler_entity_form(
                episodeHandler=episodeHandler))

        createDirectiveUseCase = CreateDirectiveUseCase.CreateDirectiveUseCase(targetPageRepository=self._targetPageRepository,
                                                                               episodeHandlerRepository=self._episodeHandlerRepository,
                                                                               directiveRuleService=MaxCodeCoverageDirectiveRuleService())
        createDirectiveInput = CreateDirectiveInput.CreateDirectiveInput(
            targetPageId=self._targetPageId, episodeHandlerId=episodeHandler.get_id())
        createDirectiveOutput = CreateDirectiveOutput.CreateDirectiveOutput()
        createDirectiveUseCase.execute(
            createDirectiveInput, createDirectiveOutput)
        self.assertFalse(createDirectiveOutput.get_is_legal_directive())

    def test_smaller_code_coverage_than_baseline_and_previous_state(self):

        episodeHandler = self._create_episode_handler()
        episodeHandler.append_state(self._create_state(actionType="click",
                                                     interactedElement=self._create_app_element(
                                                         tagName="button", value=""),
                                                     codeCoverages=[self._create_code_coverage(codeCoverageVector=[0, 1, 0, 0, 0, 0, 0, 0, 0, 0])]))
        self._episodeHandlerRepository.add(
            episodeHandlerEntity=EpisodeHandlerEntityMapper.mapping_episode_handler_entity_form(
                episodeHandler=episodeHandler))
        self._create_directive(episodeHandlerId=episodeHandler.get_id())

        episodeHandler = self._create_episode_handler()
        episodeHandler.append_state(self._create_state(actionType="click",
                                                     interactedElement=self._create_app_element(
                                                         tagName="button", value=""),
                                                     codeCoverages=[self._create_code_coverage(codeCoverageVector=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0])]))
        self._episodeHandlerRepository.add(
            episodeHandlerEntity=EpisodeHandlerEntityMapper.mapping_episode_handler_entity_form(
                episodeHandler=episodeHandler))

        createDirectiveUseCase = CreateDirectiveUseCase.CreateDirectiveUseCase(targetPageRepository=self._targetPageRepository,
                                                                               episodeHandlerRepository=self._episodeHandlerRepository,
                                                                               directiveRuleService=MaxCodeCoverageDirectiveRuleService())
        createDirectiveInput = CreateDirectiveInput.CreateDirectiveInput(
            targetPageId=self._targetPageId, episodeHandlerId=episodeHandler.get_id())
        createDirectiveOutput = CreateDirectiveOutput.CreateDirectiveOutput()

        createDirectiveUseCase.execute(
            createDirectiveInput, createDirectiveOutput)

        self.assertFalse(createDirectiveOutput.get_is_legal_directive())

    def test_improved_code_coverage_with_baseline_and_with_previous_state(
            self):
        episodeHandler = self._create_episode_handler()
        episodeHandler.append_state(self._create_state(actionType="click",
                                                     interactedElement=self._create_app_element(
                                                         tagName="button", value=""),
                                                     codeCoverages=[self._create_code_coverage(codeCoverageVector=[0, 1, 0, 0, 0, 0, 0, 0, 0, 0])]))
        self._episodeHandlerRepository.add(
            episodeHandlerEntity=EpisodeHandlerEntityMapper.mapping_episode_handler_entity_form(
                episodeHandler=episodeHandler))
        self._create_directive(episodeHandlerId=episodeHandler.get_id())

        episodeHandler = self._create_episode_handler()
        episodeHandler.append_state(self._create_state(actionType="click",
                                                     interactedElement=self._create_app_element(
                                                         tagName="button", value=""),
                                                     codeCoverages=[self._create_code_coverage(codeCoverageVector=[0, 0, 1, 0, 0, 0, 0, 0, 0, 0])]))
        self._episodeHandlerRepository.add(
            episodeHandlerEntity=EpisodeHandlerEntityMapper.mapping_episode_handler_entity_form(
                episodeHandler=episodeHandler))

        createDirectiveUseCase = CreateDirectiveUseCase.CreateDirectiveUseCase(targetPageRepository=self._targetPageRepository,
                                                                               episodeHandlerRepository=self._episodeHandlerRepository,
                                                                               directiveRuleService=MaxCodeCoverageDirectiveRuleService())
        createDirectiveInput = CreateDirectiveInput.CreateDirectiveInput(
            targetPageId=self._targetPageId, episodeHandlerId=episodeHandler.get_id())
        createDirectiveOutput = CreateDirectiveOutput.CreateDirectiveOutput()

        createDirectiveUseCase.execute(
            createDirectiveInput, createDirectiveOutput)
        self.assertFalse(createDirectiveOutput.get_is_legal_directive())

    def test_same_code_coverage_with_previous_state_but_app_event_is_smaller(
            self):
        episodeHandler = self._create_episode_handler()
        episodeHandler.append_state(self._create_state(actionType="click",
                                                     interactedElement=self._create_app_element(
                                                         tagName="button", value=""),
                                                     codeCoverages=[self._create_code_coverage(codeCoverageVector=[0, 1, 0, 0, 0, 0, 0, 0, 0, 0])]))
        episodeHandler.append_state(self._create_state(actionType="click",
                                                     interactedElement=self._create_app_element(
                                                         tagName="button", value=""),
                                                     codeCoverages=[self._create_code_coverage(codeCoverageVector=[0, 1, 0, 0, 0, 0, 0, 0, 0, 0])]))
        self._episodeHandlerRepository.add(
            episodeHandlerEntity=EpisodeHandlerEntityMapper.mapping_episode_handler_entity_form(
                episodeHandler=episodeHandler))
        self._create_directive(episodeHandlerId=episodeHandler.get_id())

        episodeHandler = self._create_episode_handler()
        episodeHandler.append_state(self._create_state(actionType="click",
                                                     interactedElement=self._create_app_element(
                                                         tagName="button", value=""),
                                                     codeCoverages=[self._create_code_coverage(codeCoverageVector=[0, 1, 0, 0, 0, 0, 0, 0, 0, 0])]))
        self._episodeHandlerRepository.add(
            episodeHandlerEntity=EpisodeHandlerEntityMapper.mapping_episode_handler_entity_form(
                episodeHandler=episodeHandler))

        createDirectiveUseCase = CreateDirectiveUseCase.CreateDirectiveUseCase(targetPageRepository=self._targetPageRepository,
                                                                               episodeHandlerRepository=self._episodeHandlerRepository,
                                                                               directiveRuleService=MaxCodeCoverageDirectiveRuleService())
        createDirectiveInput = CreateDirectiveInput.CreateDirectiveInput(
            targetPageId=self._targetPageId, episodeHandlerId=episodeHandler.get_id())
        createDirectiveOutput = CreateDirectiveOutput.CreateDirectiveOutput()

        createDirectiveUseCase.execute(
            createDirectiveInput, createDirectiveOutput)

        directiveDTO = createDirectiveOutput.get_directive_dto()
        directive = DirectiveDTOMapper.mapping_directive_from(
            directiveDTO=directiveDTO)
        self.assertTrue(createDirectiveOutput.get_is_legal_directive())
        self.assertEqual(directive.get_app_events()[0].get_value(), "")

    def test_same_code_coverage_with_previous_state_but_app_event_is_bigger(
            self):
        episodeHandler = self._create_episode_handler()
        episodeHandler.append_state(self._create_state(actionType="click",
                                                     interactedElement=self._create_app_element(
                                                         tagName="button", value=""),
                                                     codeCoverages=[self._create_code_coverage(codeCoverageVector=[0, 1, 0, 0, 0, 0, 0, 0, 0, 0])]))
        self._episodeHandlerRepository.add(
            episodeHandlerEntity=EpisodeHandlerEntityMapper.mapping_episode_handler_entity_form(
                episodeHandler=episodeHandler))
        self._create_directive(episodeHandlerId=episodeHandler.get_id())

        episodeHandler = self._create_episode_handler()
        episodeHandler.append_state(self._create_state(actionType="click",
                                                     interactedElement=self._create_app_element(
                                                         tagName="button", value=""),
                                                     codeCoverages=[self._create_code_coverage(codeCoverageVector=[0, 1, 0, 0, 0, 0, 0, 0, 0, 0])]))
        episodeHandler.append_state(self._create_state(actionType="click",
                                                     interactedElement=self._create_app_element(
                                                         tagName="button", value=""),
                                                     codeCoverages=[self._create_code_coverage(codeCoverageVector=[0, 1, 0, 0, 0, 0, 0, 0, 0, 0])]))
        self._episodeHandlerRepository.add(
            episodeHandlerEntity=EpisodeHandlerEntityMapper.mapping_episode_handler_entity_form(
                episodeHandler=episodeHandler))

        createDirectiveUseCase = CreateDirectiveUseCase.CreateDirectiveUseCase(targetPageRepository=self._targetPageRepository,
                                                                               episodeHandlerRepository=self._episodeHandlerRepository,
                                                                               directiveRuleService=MaxCodeCoverageDirectiveRuleService())
        createDirectiveInput = CreateDirectiveInput.CreateDirectiveInput(
            targetPageId=self._targetPageId, episodeHandlerId=episodeHandler.get_id())
        createDirectiveOutput = CreateDirectiveOutput.CreateDirectiveOutput()

        createDirectiveUseCase.execute(
            createDirectiveInput, createDirectiveOutput)
        self.assertFalse(createDirectiveOutput.get_is_legal_directive())

    def test_smaller_code_coverage_than_previous_state_but_app_event_is_bigger(
            self):
        episodeHandler = self._create_episode_handler()
        episodeHandler.append_state(self._create_state(actionType="click",
                                                     interactedElement=self._create_app_element(
                                                         tagName="button", value=""),
                                                     codeCoverages=[self._create_code_coverage(codeCoverageVector=[0, 1, 1, 0, 0, 0, 0, 0, 0, 0])]))
        self._episodeHandlerRepository.add(
            episodeHandlerEntity=EpisodeHandlerEntityMapper.mapping_episode_handler_entity_form(
                episodeHandler=episodeHandler))
        self._create_directive(episodeHandlerId=episodeHandler.get_id())

        episodeHandler = self._create_episode_handler()
        episodeHandler.append_state(self._create_state(actionType="click",
                                                     interactedElement=self._create_app_element(
                                                         tagName="button", value=""),
                                                     codeCoverages=[self._create_code_coverage(codeCoverageVector=[0, 1, 0, 0, 0, 0, 0, 0, 0, 0])]))
        episodeHandler.append_state(self._create_state(actionType="click",
                                                     interactedElement=self._create_app_element(
                                                         tagName="button", value=""),
                                                     codeCoverages=[self._create_code_coverage(codeCoverageVector=[0, 1, 0, 0, 0, 0, 0, 0, 0, 0])]))
        self._episodeHandlerRepository.add(
            episodeHandlerEntity=EpisodeHandlerEntityMapper.mapping_episode_handler_entity_form(
                episodeHandler=episodeHandler))

        createDirectiveUseCase = CreateDirectiveUseCase.CreateDirectiveUseCase(targetPageRepository=self._targetPageRepository,
                                                                               episodeHandlerRepository=self._episodeHandlerRepository,
                                                                               directiveRuleService=MaxCodeCoverageDirectiveRuleService())
        createDirectiveInput = CreateDirectiveInput.CreateDirectiveInput(
            targetPageId=self._targetPageId, episodeHandlerId=episodeHandler.get_id())
        createDirectiveOutput = CreateDirectiveOutput.CreateDirectiveOutput()

        createDirectiveUseCase.execute(
            createDirectiveInput, createDirectiveOutput)
        self.assertFalse(createDirectiveOutput.get_is_legal_directive())

    def test_no_improved_code_coverage_with_previous_state(self):
        episodeHandler = self._create_episode_handler()
        episodeHandler.append_state(self._create_state(actionType="click",
                                                     interactedElement=self._create_app_element(
                                                         tagName="button", value=""),
                                                     codeCoverages=[self._create_code_coverage(codeCoverageVector=[0, 1, 0, 0, 0, 0, 0, 0, 0, 0])]))
        self._episodeHandlerRepository.add(
            episodeHandlerEntity=EpisodeHandlerEntityMapper.mapping_episode_handler_entity_form(
                episodeHandler=episodeHandler))
        self._create_directive(episodeHandlerId=episodeHandler.get_id())

        episodeHandler = self._create_episode_handler()
        episodeHandler.append_state(self._create_state(actionType="click",
                                                     interactedElement=self._create_app_element(
                                                         tagName="button", value=""),
                                                     codeCoverages=[self._create_code_coverage(codeCoverageVector=[0, 1, 0, 0, 0, 0, 0, 0, 0, 0])]))
        self._episodeHandlerRepository.add(
            episodeHandlerEntity=EpisodeHandlerEntityMapper.mapping_episode_handler_entity_form(
                episodeHandler=episodeHandler))

        createDirectiveUseCase = CreateDirectiveUseCase.CreateDirectiveUseCase(targetPageRepository=self._targetPageRepository,
                                                                               episodeHandlerRepository=self._episodeHandlerRepository,
                                                                               directiveRuleService=MaxCodeCoverageDirectiveRuleService())
        createDirectiveInput = CreateDirectiveInput.CreateDirectiveInput(
            targetPageId=self._targetPageId, episodeHandlerId=episodeHandler.get_id())
        createDirectiveOutput = CreateDirectiveOutput.CreateDirectiveOutput()

        createDirectiveUseCase.execute(
            createDirectiveInput, createDirectiveOutput)

        directiveDTO = createDirectiveOutput.get_directive_dto()
        directive = DirectiveDTOMapper.mapping_directive_from(
            directiveDTO=directiveDTO)
        self.assertFalse(createDirectiveOutput.get_is_legal_directive())
        self.assertEqual(directive.get_app_events()[0].get_value(), "")

    def _create_target_page(self, repository):
        targetPageUrl = "./register.html"
        rootUrl = "./"
        appEventDTO = AppEventDTO(
            xpath="/HTML[1]/BODY[1]/DIV[1]/FORM[1]/DIV[4]/DIV[2]/P[1]/A[2]", value="")
        taskID = "testTaskID"
        originalCodeCoverageDTO = self._create_code_coverage_dto(
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
        createTargetPageUseCase.execute(
            createTargetPageInput, createTargetPageOutput)
        return createTargetPageOutput.get_id()

    def _create_code_coverage_dto(self, codeCoverageVector: [
                               bool]) -> CodeCoverageDTO:
        return CodeCoverageDTO(codeCoverageType=self._codeCoverageType,
                               codeCoverageVector=codeCoverageVector)

    def _create_code_coverage(self, codeCoverageVector: [bool]) -> CodeCoverage:
        return CodeCoverage(codeCoverageType=self._codeCoverageType,
                            codeCoverageVector=codeCoverageVector)

    def _create_episode_handler(self):
        return MorePagesExperimentEpisodeHandler(
            id="episodeHandlerId", episodeIndex=0, episodeStep=16)

    def _create_state(self, actionType: str, interactedElement: AppElement,
                     codeCoverages: [CodeCoverage]) -> State:
        state = State(id="stateId")
        state.set_action_type(actionType=actionType)
        state.set_interacted_element(interactedElement=interactedElement)
        state.set_code_coverages(codeCoverages=codeCoverages)
        return state

    def _create_app_element(self, tagName: str, value: str):
        return AppElement(tagName=tagName, name="",
                          type="", value=value, xpath="")

    def _create_directive(self, episodeHandlerId: str):
        createDirectiveUseCase = CreateDirectiveUseCase.CreateDirectiveUseCase(targetPageRepository=self._targetPageRepository,
                                                                               episodeHandlerRepository=self._episodeHandlerRepository,
                                                                               directiveRuleService=MaxCodeCoverageDirectiveRuleService())
        createDirectiveInput = CreateDirectiveInput.CreateDirectiveInput(
            targetPageId=self._targetPageId, episodeHandlerId=episodeHandlerId)
        createDirectiveOutput = CreateDirectiveOutput.CreateDirectiveOutput()
        createDirectiveUseCase.execute(
            createDirectiveInput, createDirectiveOutput)
