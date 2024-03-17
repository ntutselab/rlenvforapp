from dependency_injector.wiring import Provide, inject

from configuration.di.EnvironmentDIContainers import EnvironmentDIContainers
from RLEnvForApp.domain.environment.actionCommand import IActionCommand
from RLEnvForApp.domain.environment.actionCommandFactoryService import IActionCommandFactoryService
from RLEnvForApp.domain.environment.autOperator.IAUTOperator import IAUTOperator
from RLEnvForApp.domain.environment.observationService.IObservationService import \
    IObservationService
from RLEnvForApp.domain.environment.rewardCalculatorService.IRewardCalculatorService import \
    IRewardCalculatorService
from RLEnvForApp.domain.environment.state import State
from RLEnvForApp.usecase.environment.episodeHandler.mapper import EpisodeHandlerEntityMapper
from RLEnvForApp.usecase.environment.executeAction import ExecuteActionInput, ExecuteActionOutput
from RLEnvForApp.usecase.repository.EpisodeHandlerRepository import EpisodeHandlerRepository


class ExecuteActionUseCase:
    @inject
    def __init__(self, autOperator: IAUTOperator,
                 episodeHandlerRepository: EpisodeHandlerRepository = Provide[
                     EnvironmentDIContainers.episodeHandlerRepository],
                 rewardCalculatorService: IRewardCalculatorService = Provide[
                     EnvironmentDIContainers.rewardCalculatorService],
                 actionCommandFactory: IActionCommandFactoryService = Provide[
                     EnvironmentDIContainers.actionCommandFactory],
                 observationSerivce: IObservationService = Provide[EnvironmentDIContainers.observationService]):
        self._actionCommandFactory = actionCommandFactory
        self._autOperator = autOperator
        self._observationService = observationSerivce
        self._episodeHandlerRepository = episodeHandlerRepository
        self._rewardCalculatorService = rewardCalculatorService

    def execute(self, input: ExecuteActionInput.ExecuteActionInput, output: ExecuteActionOutput.ExecuteActionOutput):
        episode_handler_entity = self._episodeHandlerRepository.findById(input.getEpisodeHandlerId())
        episode_handler = EpisodeHandlerEntityMapper.mappingEpisodeHandlerForm(
            episodeHandlerEntity=episode_handler_entity)

        previous_state: State = episode_handler.getAllState()[-1]
        previous_state.setActionNumber(input.getActionNumber())

        action_command: IActionCommand = self._actionCommandFactory.createActionCommand(
            actionNumber=input.getActionNumber())
        action_command.execute(operator=self._autOperator)

        if input.getActionNumber() == 0:
            previous_state.setActionType("click")
        else:
            previous_state.setActionType("input")
            previous_state.setAppEventInputValue(action_command.getInputValue())

        state: State = self._autOperator.getState()
        observation, original_observation = self._observationService.getObservation(state=state)
        state.setOriginalObservation(original_observation)

        episode_handler.appendState(state=state)
        self._episodeHandlerRepository.update(
            EpisodeHandlerEntityMapper.mappingEpisodeHandlerEntityForm(episodeHandler=episode_handler))

        code_coverage_dict = {}
        for code_coverage in state.getCodeCoverages():
            code_coverage_dict[code_coverage.getCodeCoverageType(
            )] = self._getPercent(code_coverage.getRatio())
        output.setObservation(observation)
        output.setOriginalObservation(original_observation)
        output.setCodeCoverageDict(codeCoverageDict=code_coverage_dict)
        output.setReward(self._rewardCalculatorService.calculateReward(
            episodeHandler=episode_handler))
        output.setCosineSimilarityText(self._rewardCalculatorService.getCosineSimilarityText())
        output.setIsDone(episode_handler.isDone())

    def _getPercent(self, ratio):
        return ratio * 100
