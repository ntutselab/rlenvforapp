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
        self._code_coverage_type = "statement coverage"
        self._target_page_repository = InMemoryTargetPageRepository()
        self._episode_handler_repository = InMemoryEpisodeHandlerRepository()
        self._target_page_id = self._create_target_page(
            repository=self._target_page_repository)

    def test_no_improved_code_coverage_with_baseline(self):
        episode_handler = self._create_episode_handler()
        episode_handler.append_state(self._create_state(action_type="click",
                                                     interactedElement=self._create_app_element(
                                                         tag_name="button", value=""),
                                                     code_coverages=[self._create_code_coverage(code_coverage_vector=[1, 0, 0, 0, 0, 0, 0, 0, 0, 0])]))
        self._episode_handler_repository.add(
            episode_handler_entity=EpisodeHandlerEntityMapper.mapping_episode_handler_entity_form(
                episode_handler=episode_handler))

        create_directive_use_case = CreateDirectiveUseCase.CreateDirectiveUseCase(targetPageRepository=self._target_page_repository,
                                                                               episodeHandlerRepository=self._episode_handler_repository,
                                                                               directiveRuleService=MaxCodeCoverageDirectiveRuleService())
        create_directive_input = CreateDirectiveInput.CreateDirectiveInput(
            target_page_id=self._target_page_id, episode_handler_id=episode_handler.get_id())
        create_directive_output = CreateDirectiveOutput.CreateDirectiveOutput()

        create_directive_use_case.execute(
            create_directive_input, create_directive_output)

        self.assertFalse(create_directive_output.get_is_legal_directive())

    def test_improved_code_coverage_with_baseline_and_more_app_event(self):
        episode_handler = self._create_episode_handler()
        episode_handler.append_state(self._create_state(action_type="input",
                                                     interactedElement=self._create_app_element(
                                                         tag_name="input", value="123"),
                                                     code_coverages=[self._create_code_coverage(code_coverage_vector=[0, 1, 0, 0, 0, 0, 0, 0, 0, 0])]))
        episode_handler.append_state(self._create_state(action_type="input",
                                                     interactedElement=self._create_app_element(
                                                         tag_name="input", value="456"),
                                                     code_coverages=[self._create_code_coverage(code_coverage_vector=[0, 1, 0, 0, 0, 0, 0, 0, 0, 0])]))
        episode_handler.append_state(self._create_state(action_type="click",
                                                     interactedElement=self._create_app_element(
                                                         tag_name="button", value=""),
                                                     code_coverages=[self._create_code_coverage(code_coverage_vector=[0, 1, 0, 0, 0, 0, 0, 0, 0, 0])]))
        self._episode_handler_repository.add(
            episode_handler_entity=EpisodeHandlerEntityMapper.mapping_episode_handler_entity_form(
                episode_handler=episode_handler))

        create_directive_use_case = CreateDirectiveUseCase.CreateDirectiveUseCase(targetPageRepository=self._target_page_repository,
                                                                               episodeHandlerRepository=self._episode_handler_repository,
                                                                               directiveRuleService=MaxCodeCoverageDirectiveRuleService())
        create_directive_input = CreateDirectiveInput.CreateDirectiveInput(
            target_page_id=self._target_page_id, episode_handler_id=episode_handler.get_id())
        create_directive_output = CreateDirectiveOutput.CreateDirectiveOutput()

        create_directive_use_case.execute(
            create_directive_input, create_directive_output)

        directive_dto = create_directive_output.get_directive_dto()
        directive = DirectiveDTOMapper.mapping_directive_from(
            directive_dto=directive_dto)
        self.assertTrue(create_directive_output.get_is_legal_directive())
        self.assertEqual(len(directive.get_app_events()), 3)

    def test_smaller_code_coverage_than_baseline(self):
        episode_handler = self._create_episode_handler()
        episode_handler.append_state(self._create_state(action_type="click",
                                                     interactedElement=self._create_app_element(
                                                         tag_name="button", value=""),
                                                     code_coverages=[self._create_code_coverage(code_coverage_vector=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0])]))
        self._episode_handler_repository.add(
            episode_handler_entity=EpisodeHandlerEntityMapper.mapping_episode_handler_entity_form(
                episode_handler=episode_handler))

        create_directive_use_case = CreateDirectiveUseCase.CreateDirectiveUseCase(targetPageRepository=self._target_page_repository,
                                                                               episodeHandlerRepository=self._episode_handler_repository,
                                                                               directiveRuleService=MaxCodeCoverageDirectiveRuleService())
        create_directive_input = CreateDirectiveInput.CreateDirectiveInput(
            target_page_id=self._target_page_id, episode_handler_id=episode_handler.get_id())
        create_directive_output = CreateDirectiveOutput.CreateDirectiveOutput()

        create_directive_use_case.execute(
            create_directive_input, create_directive_output)

        self.assertFalse(create_directive_output.get_is_legal_directive())

    def test_no_improved_code_coverage_with_baseline_and_more_previous_state(
            self):
        episode_handler = self._create_episode_handler()
        episode_handler.append_state(self._create_state(action_type="click",
                                                     interactedElement=self._create_app_element(
                                                         tag_name="button", value=""),
                                                     code_coverages=[self._create_code_coverage(code_coverage_vector=[0, 1, 0, 0, 0, 0, 0, 0, 0, 0])]))
        self._episode_handler_repository.add(
            episode_handler_entity=EpisodeHandlerEntityMapper.mapping_episode_handler_entity_form(
                episode_handler=episode_handler))
        self._create_directive(episode_handler_id=episode_handler.get_id())

        episode_handler = self._create_episode_handler()
        episode_handler.append_state(self._create_state(action_type="click",
                                                     interactedElement=self._create_app_element(
                                                         tag_name="button", value=""),
                                                     code_coverages=[self._create_code_coverage(code_coverage_vector=[1, 0, 0, 0, 0, 0, 0, 0, 0, 0])]))
        self._episode_handler_repository.add(
            episode_handler_entity=EpisodeHandlerEntityMapper.mapping_episode_handler_entity_form(
                episode_handler=episode_handler))

        create_directive_use_case = CreateDirectiveUseCase.CreateDirectiveUseCase(targetPageRepository=self._target_page_repository,
                                                                               episodeHandlerRepository=self._episode_handler_repository,
                                                                               directiveRuleService=MaxCodeCoverageDirectiveRuleService())
        create_directive_input = CreateDirectiveInput.CreateDirectiveInput(
            target_page_id=self._target_page_id, episode_handler_id=episode_handler.get_id())
        create_directive_output = CreateDirectiveOutput.CreateDirectiveOutput()
        create_directive_use_case.execute(
            create_directive_input, create_directive_output)
        self.assertFalse(create_directive_output.get_is_legal_directive())

        episode_handler = self._create_episode_handler()
        episode_handler.append_state(self._create_state(action_type="click",
                                                     interactedElement=self._create_app_element(
                                                         tag_name="button", value=""),
                                                     code_coverages=[self._create_code_coverage(code_coverage_vector=[0, 1, 0, 0, 0, 0, 0, 0, 0, 0])]))
        self._episode_handler_repository.add(
            episode_handler_entity=EpisodeHandlerEntityMapper.mapping_episode_handler_entity_form(
                episode_handler=episode_handler))

        create_directive_use_case = CreateDirectiveUseCase.CreateDirectiveUseCase(targetPageRepository=self._target_page_repository,
                                                                               episodeHandlerRepository=self._episode_handler_repository,
                                                                               directiveRuleService=MaxCodeCoverageDirectiveRuleService())
        create_directive_input = CreateDirectiveInput.CreateDirectiveInput(
            target_page_id=self._target_page_id, episode_handler_id=episode_handler.get_id())
        create_directive_output = CreateDirectiveOutput.CreateDirectiveOutput()
        create_directive_use_case.execute(
            create_directive_input, create_directive_output)
        self.assertFalse(create_directive_output.get_is_legal_directive())

    def test_smaller_code_coverage_than_baseline_and_previous_state(self):

        episode_handler = self._create_episode_handler()
        episode_handler.append_state(self._create_state(action_type="click",
                                                     interactedElement=self._create_app_element(
                                                         tag_name="button", value=""),
                                                     code_coverages=[self._create_code_coverage(code_coverage_vector=[0, 1, 0, 0, 0, 0, 0, 0, 0, 0])]))
        self._episode_handler_repository.add(
            episode_handler_entity=EpisodeHandlerEntityMapper.mapping_episode_handler_entity_form(
                episode_handler=episode_handler))
        self._create_directive(episode_handler_id=episode_handler.get_id())

        episode_handler = self._create_episode_handler()
        episode_handler.append_state(self._create_state(action_type="click",
                                                     interactedElement=self._create_app_element(
                                                         tag_name="button", value=""),
                                                     code_coverages=[self._create_code_coverage(code_coverage_vector=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0])]))
        self._episode_handler_repository.add(
            episode_handler_entity=EpisodeHandlerEntityMapper.mapping_episode_handler_entity_form(
                episode_handler=episode_handler))

        create_directive_use_case = CreateDirectiveUseCase.CreateDirectiveUseCase(targetPageRepository=self._target_page_repository,
                                                                               episodeHandlerRepository=self._episode_handler_repository,
                                                                               directiveRuleService=MaxCodeCoverageDirectiveRuleService())
        create_directive_input = CreateDirectiveInput.CreateDirectiveInput(
            target_page_id=self._target_page_id, episode_handler_id=episode_handler.get_id())
        create_directive_output = CreateDirectiveOutput.CreateDirectiveOutput()

        create_directive_use_case.execute(
            create_directive_input, create_directive_output)

        self.assertFalse(create_directive_output.get_is_legal_directive())

    def test_improved_code_coverage_with_baseline_and_with_previous_state(
            self):
        episode_handler = self._create_episode_handler()
        episode_handler.append_state(self._create_state(action_type="click",
                                                     interactedElement=self._create_app_element(
                                                         tag_name="button", value=""),
                                                     code_coverages=[self._create_code_coverage(code_coverage_vector=[0, 1, 0, 0, 0, 0, 0, 0, 0, 0])]))
        self._episode_handler_repository.add(
            episode_handler_entity=EpisodeHandlerEntityMapper.mapping_episode_handler_entity_form(
                episode_handler=episode_handler))
        self._create_directive(episode_handler_id=episode_handler.get_id())

        episode_handler = self._create_episode_handler()
        episode_handler.append_state(self._create_state(action_type="click",
                                                     interactedElement=self._create_app_element(
                                                         tag_name="button", value=""),
                                                     code_coverages=[self._create_code_coverage(code_coverage_vector=[0, 0, 1, 0, 0, 0, 0, 0, 0, 0])]))
        self._episode_handler_repository.add(
            episode_handler_entity=EpisodeHandlerEntityMapper.mapping_episode_handler_entity_form(
                episode_handler=episode_handler))

        create_directive_use_case = CreateDirectiveUseCase.CreateDirectiveUseCase(targetPageRepository=self._target_page_repository,
                                                                               episodeHandlerRepository=self._episode_handler_repository,
                                                                               directiveRuleService=MaxCodeCoverageDirectiveRuleService())
        create_directive_input = CreateDirectiveInput.CreateDirectiveInput(
            target_page_id=self._target_page_id, episode_handler_id=episode_handler.get_id())
        create_directive_output = CreateDirectiveOutput.CreateDirectiveOutput()

        create_directive_use_case.execute(
            create_directive_input, create_directive_output)
        self.assertFalse(create_directive_output.get_is_legal_directive())

    def test_same_code_coverage_with_previous_state_but_app_event_is_smaller(
            self):
        episode_handler = self._create_episode_handler()
        episode_handler.append_state(self._create_state(action_type="click",
                                                     interactedElement=self._create_app_element(
                                                         tag_name="button", value=""),
                                                     code_coverages=[self._create_code_coverage(code_coverage_vector=[0, 1, 0, 0, 0, 0, 0, 0, 0, 0])]))
        episode_handler.append_state(self._create_state(action_type="click",
                                                     interactedElement=self._create_app_element(
                                                         tag_name="button", value=""),
                                                     code_coverages=[self._create_code_coverage(code_coverage_vector=[0, 1, 0, 0, 0, 0, 0, 0, 0, 0])]))
        self._episode_handler_repository.add(
            episode_handler_entity=EpisodeHandlerEntityMapper.mapping_episode_handler_entity_form(
                episode_handler=episode_handler))
        self._create_directive(episode_handler_id=episode_handler.get_id())

        episode_handler = self._create_episode_handler()
        episode_handler.append_state(self._create_state(action_type="click",
                                                     interactedElement=self._create_app_element(
                                                         tag_name="button", value=""),
                                                     code_coverages=[self._create_code_coverage(code_coverage_vector=[0, 1, 0, 0, 0, 0, 0, 0, 0, 0])]))
        self._episode_handler_repository.add(
            episode_handler_entity=EpisodeHandlerEntityMapper.mapping_episode_handler_entity_form(
                episode_handler=episode_handler))

        create_directive_use_case = CreateDirectiveUseCase.CreateDirectiveUseCase(targetPageRepository=self._target_page_repository,
                                                                               episodeHandlerRepository=self._episode_handler_repository,
                                                                               directiveRuleService=MaxCodeCoverageDirectiveRuleService())
        create_directive_input = CreateDirectiveInput.CreateDirectiveInput(
            target_page_id=self._target_page_id, episode_handler_id=episode_handler.get_id())
        create_directive_output = CreateDirectiveOutput.CreateDirectiveOutput()

        create_directive_use_case.execute(
            create_directive_input, create_directive_output)

        directive_dto = create_directive_output.get_directive_dto()
        directive = DirectiveDTOMapper.mapping_directive_from(
            directive_dto=directive_dto)
        self.assertTrue(create_directive_output.get_is_legal_directive())
        self.assertEqual(directive.get_app_events()[0].get_value(), "")

    def test_same_code_coverage_with_previous_state_but_app_event_is_bigger(
            self):
        episode_handler = self._create_episode_handler()
        episode_handler.append_state(self._create_state(action_type="click",
                                                     interactedElement=self._create_app_element(
                                                         tag_name="button", value=""),
                                                     code_coverages=[self._create_code_coverage(code_coverage_vector=[0, 1, 0, 0, 0, 0, 0, 0, 0, 0])]))
        self._episode_handler_repository.add(
            episode_handler_entity=EpisodeHandlerEntityMapper.mapping_episode_handler_entity_form(
                episode_handler=episode_handler))
        self._create_directive(episode_handler_id=episode_handler.get_id())

        episode_handler = self._create_episode_handler()
        episode_handler.append_state(self._create_state(action_type="click",
                                                     interactedElement=self._create_app_element(
                                                         tag_name="button", value=""),
                                                     code_coverages=[self._create_code_coverage(code_coverage_vector=[0, 1, 0, 0, 0, 0, 0, 0, 0, 0])]))
        episode_handler.append_state(self._create_state(action_type="click",
                                                     interactedElement=self._create_app_element(
                                                         tag_name="button", value=""),
                                                     code_coverages=[self._create_code_coverage(code_coverage_vector=[0, 1, 0, 0, 0, 0, 0, 0, 0, 0])]))
        self._episode_handler_repository.add(
            episode_handler_entity=EpisodeHandlerEntityMapper.mapping_episode_handler_entity_form(
                episode_handler=episode_handler))

        create_directive_use_case = CreateDirectiveUseCase.CreateDirectiveUseCase(targetPageRepository=self._target_page_repository,
                                                                               episodeHandlerRepository=self._episode_handler_repository,
                                                                               directiveRuleService=MaxCodeCoverageDirectiveRuleService())
        create_directive_input = CreateDirectiveInput.CreateDirectiveInput(
            target_page_id=self._target_page_id, episode_handler_id=episode_handler.get_id())
        create_directive_output = CreateDirectiveOutput.CreateDirectiveOutput()

        create_directive_use_case.execute(
            create_directive_input, create_directive_output)
        self.assertFalse(create_directive_output.get_is_legal_directive())

    def test_smaller_code_coverage_than_previous_state_but_app_event_is_bigger(
            self):
        episode_handler = self._create_episode_handler()
        episode_handler.append_state(self._create_state(action_type="click",
                                                     interactedElement=self._create_app_element(
                                                         tag_name="button", value=""),
                                                     code_coverages=[self._create_code_coverage(code_coverage_vector=[0, 1, 1, 0, 0, 0, 0, 0, 0, 0])]))
        self._episode_handler_repository.add(
            episode_handler_entity=EpisodeHandlerEntityMapper.mapping_episode_handler_entity_form(
                episode_handler=episode_handler))
        self._create_directive(episode_handler_id=episode_handler.get_id())

        episode_handler = self._create_episode_handler()
        episode_handler.append_state(self._create_state(action_type="click",
                                                     interactedElement=self._create_app_element(
                                                         tag_name="button", value=""),
                                                     code_coverages=[self._create_code_coverage(code_coverage_vector=[0, 1, 0, 0, 0, 0, 0, 0, 0, 0])]))
        episode_handler.append_state(self._create_state(action_type="click",
                                                     interactedElement=self._create_app_element(
                                                         tag_name="button", value=""),
                                                     code_coverages=[self._create_code_coverage(code_coverage_vector=[0, 1, 0, 0, 0, 0, 0, 0, 0, 0])]))
        self._episode_handler_repository.add(
            episode_handler_entity=EpisodeHandlerEntityMapper.mapping_episode_handler_entity_form(
                episode_handler=episode_handler))

        create_directive_use_case = CreateDirectiveUseCase.CreateDirectiveUseCase(targetPageRepository=self._target_page_repository,
                                                                               episodeHandlerRepository=self._episode_handler_repository,
                                                                               directiveRuleService=MaxCodeCoverageDirectiveRuleService())
        create_directive_input = CreateDirectiveInput.CreateDirectiveInput(
            target_page_id=self._target_page_id, episode_handler_id=episode_handler.get_id())
        create_directive_output = CreateDirectiveOutput.CreateDirectiveOutput()

        create_directive_use_case.execute(
            create_directive_input, create_directive_output)
        self.assertFalse(create_directive_output.get_is_legal_directive())

    def test_no_improved_code_coverage_with_previous_state(self):
        episode_handler = self._create_episode_handler()
        episode_handler.append_state(self._create_state(action_type="click",
                                                     interactedElement=self._create_app_element(
                                                         tag_name="button", value=""),
                                                     code_coverages=[self._create_code_coverage(code_coverage_vector=[0, 1, 0, 0, 0, 0, 0, 0, 0, 0])]))
        self._episode_handler_repository.add(
            episode_handler_entity=EpisodeHandlerEntityMapper.mapping_episode_handler_entity_form(
                episode_handler=episode_handler))
        self._create_directive(episode_handler_id=episode_handler.get_id())

        episode_handler = self._create_episode_handler()
        episode_handler.append_state(self._create_state(action_type="click",
                                                     interactedElement=self._create_app_element(
                                                         tag_name="button", value=""),
                                                     code_coverages=[self._create_code_coverage(code_coverage_vector=[0, 1, 0, 0, 0, 0, 0, 0, 0, 0])]))
        self._episode_handler_repository.add(
            episode_handler_entity=EpisodeHandlerEntityMapper.mapping_episode_handler_entity_form(
                episode_handler=episode_handler))

        create_directive_use_case = CreateDirectiveUseCase.CreateDirectiveUseCase(targetPageRepository=self._target_page_repository,
                                                                               episodeHandlerRepository=self._episode_handler_repository,
                                                                               directiveRuleService=MaxCodeCoverageDirectiveRuleService())
        create_directive_input = CreateDirectiveInput.CreateDirectiveInput(
            target_page_id=self._target_page_id, episode_handler_id=episode_handler.get_id())
        create_directive_output = CreateDirectiveOutput.CreateDirectiveOutput()

        create_directive_use_case.execute(
            create_directive_input, create_directive_output)

        directive_dto = create_directive_output.get_directive_dto()
        directive = DirectiveDTOMapper.mapping_directive_from(
            directive_dto=directive_dto)
        self.assertFalse(create_directive_output.get_is_legal_directive())
        self.assertEqual(directive.get_app_events()[0].get_value(), "")

    def _create_target_page(self, repository):
        target_page_url = "./register.html"
        root_url = "./"
        app_event_dto = AppEventDTO(
            xpath="/HTML[1]/BODY[1]/DIV[1]/FORM[1]/DIV[4]/DIV[2]/P[1]/A[2]", value="")
        task_id = "testTaskID"
        original_code_coverage_dto = self._create_code_coverage_dto(
            code_coverage_vector=[1, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        create_target_page_use_case = CreateTargetPageUseCase.CreateTargetPageUseCase(
            repository=repository)
        create_target_page_input = CreateTargetPageInput.CreateTargetPageInput(target_page_url=target_page_url,
                                                                            root_url=root_url,
                                                                            app_event_dt_os=[
                                                                                app_event_dto],
                                                                            task_id=task_id,
                                                                            basic_code_coverage=original_code_coverage_dto)
        create_target_page_output = CreateTargetPageOutput.CreateTargetPageOutput()
        create_target_page_use_case.execute(
            create_target_page_input, create_target_page_output)
        return create_target_page_output.get_id()

    def _create_code_coverage_dto(self, code_coverage_vector: [
                               bool]) -> CodeCoverageDTO:
        return CodeCoverageDTO(code_coverage_type=self._code_coverage_type,
                               code_coverage_vector=code_coverage_vector)

    def _create_code_coverage(self, code_coverage_vector: [bool]) -> CodeCoverage:
        return CodeCoverage(code_coverage_type=self._code_coverage_type,
                            code_coverage_vector=code_coverage_vector)

    def _create_episode_handler(self):
        return MorePagesExperimentEpisodeHandler(
            id="episodeHandlerId", episodeIndex=0, episode_step=16)

    def _create_state(self, action_type: str, interactedElement: AppElement,
                     code_coverages: [CodeCoverage]) -> State:
        state = State(id="stateId")
        state.set_action_type(action_type=action_type)
        state.set_interacted_element(interactedElement=interactedElement)
        state.set_code_coverages(code_coverages=code_coverages)
        return state

    def _create_app_element(self, tag_name: str, value: str):
        return AppElement(tag_name=tag_name, name="",
                          type="", value=value, xpath="")

    def _create_directive(self, episode_handler_id: str):
        create_directive_use_case = CreateDirectiveUseCase.CreateDirectiveUseCase(targetPageRepository=self._target_page_repository,
                                                                               episodeHandlerRepository=self._episode_handler_repository,
                                                                               directiveRuleService=MaxCodeCoverageDirectiveRuleService())
        create_directive_input = CreateDirectiveInput.CreateDirectiveInput(
            target_page_id=self._target_page_id, episode_handler_id=episode_handler_id)
        create_directive_output = CreateDirectiveOutput.CreateDirectiveOutput()
        create_directive_use_case.execute(
            create_directive_input, create_directive_output)
