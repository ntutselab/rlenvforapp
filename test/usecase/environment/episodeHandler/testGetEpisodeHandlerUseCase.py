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
        self._episodeHandlerRepository = InMemoryEpisodeHandlerRepository()
        self._codeCoverageType = "statement coverage"

    def test_get_episode_handler_dto(self):
        episodeHandler = self._create_episode_handler()
        episodeHandlerId = episodeHandler.get_id()
        episodeHandler.append_state(self._create_state(actionType="click",
                                                     interactedElement=self._create_app_element(
                                                         value=""),
                                                     codeCoverages=[self._create_code_coverage(codeCoverageVector=[0, 1, 0, 0, 0, 0, 0, 0, 0, 0])]))
        episodeHandler.append_state(self._create_state(actionType="changeFocus",
                                                     interactedElement=self._create_app_element(
                                                         value=""),
                                                     codeCoverages=[self._create_code_coverage(codeCoverageVector=[0, 1, 0, 0, 0, 0, 0, 0, 0, 0])]))
        episodeHandler.append_state(self._create_state(actionType="click",
                                                     interactedElement=self._create_app_element(
                                                         value=""),
                                                     codeCoverages=[self._create_code_coverage(codeCoverageVector=[0, 1, 0, 0, 0, 0, 0, 0, 0, 0])]))
        self._episodeHandlerRepository.add(
            episodeHandlerEntity=EpisodeHandlerEntityMapper.mapping_episode_handler_entity_form(
                episodeHandler=episodeHandler))

        usecase = GetEpisodeHandlerUseCase.GetEpisodeHandlerUseCase(
            episodeHandlerRepository=self._episodeHandlerRepository)
        input = GetEpisodeHandlerInput.GetEpisodeHandlerInput(
            episodeHandlerId=episodeHandlerId)
        output = GetEpisodeHandlerOutput.GetEpisodeHandlerOutput()

        usecase.execute(input=input, output=output)
        self.assertEqual(3, len(output.get_episode_handler_dto().get_state_dt_os()))
        self.assertEqual(
            episodeHandlerId,
            output.get_episode_handler_dto().get_id())

    def _create_episode_handler(self):
        return MorePagesExperimentEpisodeHandler(
            id=str(uuid.uuid4()), episodeIndex=0, episodeStep=16)

    def _create_state(self, actionType: str, interactedElement: AppElement,
                     codeCoverages: [CodeCoverage]) -> State:
        state = State(id="stateId")
        state.set_action_type(actionType=actionType)
        state.set_interacted_element(interactedElement=interactedElement)
        state.set_code_coverages(codeCoverages=codeCoverages)
        return state

    def _create_code_coverage(self, codeCoverageVector: [bool]) -> CodeCoverage:
        return CodeCoverage(codeCoverageType=self._codeCoverageType,
                            codeCoverageVector=codeCoverageVector)

    def _create_app_element(self, value: str):
        return AppElement(tagName="", name="", type="", value=value, xpath="")
