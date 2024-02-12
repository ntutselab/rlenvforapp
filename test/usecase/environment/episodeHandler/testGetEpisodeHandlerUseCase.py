import unittest
import uuid

from RLEnvForApp.adapter.repository.episodeHandler.InMemoryEpisodeHandlerRepository import \
    InMemoryEpisodeHandlerRepository
from RLEnvForApp.domain.environment.episodeHandler.MorePagesExperimentEpisodeHandler import \
    MorePagesExperimentEpisodeHandler
from RLEnvForApp.domain.environment.state.AppElement import AppElement
from RLEnvForApp.domain.environment.state.CodeCoverage import CodeCoverage
from RLEnvForApp.domain.environment.state.State import State
from RLEnvForApp.usecase.environment.episodeHandler.get import GetEpisodeHandlerUseCase, GetEpisodeHandlerInput, GetEpisodeHandlerOutput
from RLEnvForApp.usecase.environment.episodeHandler.mapper import EpisodeHandlerEntityMapper


class testGetEpisodeHandlerUseCase(unittest.TestCase):
    def setUp(self) -> None:
        self._episodeHandlerRepository = InMemoryEpisodeHandlerRepository()
        self._codeCoverageType = "statement coverage"

    def test_get_episodeHandlerDTO(self):
        episodeHandler = self._createEpisodeHandler()
        episodeHandlerId = episodeHandler.getId()
        episodeHandler.appendState(self._createState(actionType="click",
                                                     interactedElement=self._createAppElement(
                                                         value=""),
                                                     codeCoverages=[self._createCodeCoverage(codeCoverageVector=[0, 1, 0, 0, 0, 0, 0, 0, 0, 0])]))
        episodeHandler.appendState(self._createState(actionType="changeFocus",
                                                     interactedElement=self._createAppElement(
                                                         value=""),
                                                     codeCoverages=[self._createCodeCoverage(codeCoverageVector=[0, 1, 0, 0, 0, 0, 0, 0, 0, 0])]))
        episodeHandler.appendState(self._createState(actionType="click",
                                                     interactedElement=self._createAppElement(
                                                         value=""),
                                                     codeCoverages=[self._createCodeCoverage(codeCoverageVector=[0, 1, 0, 0, 0, 0, 0, 0, 0, 0])]))
        self._episodeHandlerRepository.add(
            episodeHandlerEntity=EpisodeHandlerEntityMapper.mappingEpisodeHandlerEntityForm(
                episodeHandler=episodeHandler))

        usecase = GetEpisodeHandlerUseCase.GetEpisodeHandlerUseCase(
            episodeHandlerRepository=self._episodeHandlerRepository)
        input = GetEpisodeHandlerInput.GetEpisodeHandlerInput(episodeHandlerId=episodeHandlerId)
        output = GetEpisodeHandlerOutput.GetEpisodeHandlerOutput()

        usecase.execute(input=input, output=output)
        self.assertEqual(3, len(output.getEpisodeHandlerDTO().getStateDTOs()))
        self.assertEqual(episodeHandlerId, output.getEpisodeHandlerDTO().getId())

    def _createEpisodeHandler(self):
        return MorePagesExperimentEpisodeHandler(
            id=str(uuid.uuid4()), episodeIndex=0, episodeStep=16)

    def _createState(self, actionType: str, interactedElement: AppElement,
                     codeCoverages: [CodeCoverage]) -> State:
        state = State(id="stateId")
        state.setActionType(actionType=actionType)
        state.setInteractedElement(interactedElement=interactedElement)
        state.setCodeCoverages(codeCoverages=codeCoverages)
        return state

    def _createCodeCoverage(self, codeCoverageVector: [bool]) -> CodeCoverage:
        return CodeCoverage(codeCoverageType=self._codeCoverageType,
                            codeCoverageVector=codeCoverageVector)

    def _createAppElement(self, value: str):
        return AppElement(tagName="", name="", type="", value=value, xpath="")
