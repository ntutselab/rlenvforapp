import unittest
import uuid

from RLEnvForApp.adapter.repository.episodeHandler.InMemoryEpisodeHandlerRepository import \
    InMemoryEpisodeHandlerRepository
from RLEnvForApp.domain.environment.episodeHandler.MorePagesExperimentEpisodeHandler import \
    MorePagesExperimentEpisodeHandler
from RLEnvForApp.domain.environment.state.AppElement import AppElement
from RLEnvForApp.domain.environment.state.CodeCoverage import CodeCoverage
from RLEnvForApp.domain.environment.state.State import State
from RLEnvForApp.usecase.environment.episodeHandler.get import (
    GetEpisodeHandlerInput, GetEpisodeHandlerOutput, GetEpisodeHandlerUseCase)
from RLEnvForApp.usecase.environment.episodeHandler.mapper import \
    EpisodeHandlerEntityMapper


class testGetEpisodeHandlerUseCase(unittest.TestCase):
    def set_up(self) -> None:
        self._episode_handler_repository = InMemoryEpisodeHandlerRepository()
        self._code_coverage_type = "statement coverage"

    def test_get_episode_handler_dto(self):
        episode_handler = self._create_episode_handler()
        episode_handler_id = episode_handler.get_id()
        episode_handler.append_state(self._create_state(action_type="click",
                                                     interactedElement=self._create_app_element(
                                                         value=""),
                                                     code_coverages=[self._create_code_coverage(code_coverage_vector=[0, 1, 0, 0, 0, 0, 0, 0, 0, 0])]))
        episode_handler.append_state(self._create_state(action_type="changeFocus",
                                                     interactedElement=self._create_app_element(
                                                         value=""),
                                                     code_coverages=[self._create_code_coverage(code_coverage_vector=[0, 1, 0, 0, 0, 0, 0, 0, 0, 0])]))
        episode_handler.append_state(self._create_state(action_type="click",
                                                     interactedElement=self._create_app_element(
                                                         value=""),
                                                     code_coverages=[self._create_code_coverage(code_coverage_vector=[0, 1, 0, 0, 0, 0, 0, 0, 0, 0])]))
        self._episode_handler_repository.add(
            episode_handler_entity=EpisodeHandlerEntityMapper.mapping_episode_handler_entity_form(
                episode_handler=episode_handler))

        usecase = GetEpisodeHandlerUseCase.GetEpisodeHandlerUseCase(
            episodeHandlerRepository=self._episode_handler_repository)
        input = GetEpisodeHandlerInput.GetEpisodeHandlerInput(
            episode_handler_id=episode_handler_id)
        output = GetEpisodeHandlerOutput.GetEpisodeHandlerOutput()

        usecase.execute(input=input, output=output)
        self.assertEqual(3, len(output.get_episode_handler_dto().get_state_dt_os()))
        self.assertEqual(
            episode_handler_id,
            output.get_episode_handler_dto().get_id())

    def _create_episode_handler(self):
        return MorePagesExperimentEpisodeHandler(
            id=str(uuid.uuid4()), episodeIndex=0, episode_step=16)

    def _create_state(self, action_type: str, interactedElement: AppElement,
                     code_coverages: [CodeCoverage]) -> State:
        state = State(id="stateId")
        state.set_action_type(action_type=action_type)
        state.set_interacted_element(interactedElement=interactedElement)
        state.set_code_coverages(code_coverages=code_coverages)
        return state

    def _create_code_coverage(self, code_coverage_vector: [bool]) -> CodeCoverage:
        return CodeCoverage(code_coverage_type=self._code_coverage_type,
                            code_coverage_vector=code_coverage_vector)

    def _create_app_element(self, value: str):
        return AppElement(tag_name="", name="", type="", value=value, xpath="")
