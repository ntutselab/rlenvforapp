from dependency_injector.wiring import Provide, inject

from configuration.di.EnvironmentDIContainers import EnvironmentDIContainers
from RLEnvForApp.domain.environment.actionCommand import IActionCommand
from RLEnvForApp.domain.environment.actionCommandFactoryService import \
    IActionCommandFactoryService
from RLEnvForApp.domain.environment.autOperator.IAUTOperator import \
    IAUTOperator
from RLEnvForApp.domain.environment.observationService.IObservationService import \
    IObservationService
from RLEnvForApp.domain.environment.rewardCalculatorService.IRewardCalculatorService import \
    IRewardCalculatorService
from RLEnvForApp.domain.environment.state import State
from RLEnvForApp.usecase.environment.episodeHandler.mapper import \
    EpisodeHandlerEntityMapper
from RLEnvForApp.usecase.environment.executeAction import (ExecuteActionInput,
                                                           ExecuteActionOutput)
from RLEnvForApp.usecase.repository.EpisodeHandlerRepository import \
    EpisodeHandlerRepository


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

    def execute(self, input: ExecuteActionInput.ExecuteActionInput,
                output: ExecuteActionOutput.ExecuteActionOutput):
        episodeHandlerEntity = self._episodeHandlerRepository.find_by_id(
            input.get_episode_handler_id())
        episodeHandler = EpisodeHandlerEntityMapper.mapping_episode_handler_form(
            episodeHandlerEntity=episodeHandlerEntity)

        previousState: State = episodeHandler.get_all_state()[-1]
        previousState.set_action_number(input.get_action_number())

        actionCommand: IActionCommand = self._actionCommandFactory.create_action_command(
            actionNumber=input.get_action_number())
        actionCommand.execute(operator=self._autOperator)

        if input.get_action_number() == 0:
            previousState.set_action_type("click")
        else:
            previousState.set_action_type("input")
            previousState.set_app_event_input_value(actionCommand.get_input_value())

        state: State = self._autOperator.get_state()
        observation, originalObservation = self._observationService.get_observation(
            state=state)
        state.set_original_observation(originalObservation)

        episodeHandler.append_state(state=state)
        self._episodeHandlerRepository.update(
            EpisodeHandlerEntityMapper.mapping_episode_handler_entity_form(
                episodeHandler=episodeHandler))

        codeCoverageDict = {}
        for codeCoverage in state.get_code_coverages():
            codeCoverageDict[codeCoverage.get_code_coverage_type(
            )] = self._get_percent(codeCoverage.get_ratio())
        output.set_observation(observation)
        output.set_original_observation(originalObservation)
        output.set_code_coverage_dict(codeCoverageDict=codeCoverageDict)
        output.set_reward(
            self._rewardCalculatorService.calculate_reward(
                episodeHandler=episodeHandler))
        output.set_cosine_similarity_text(
            self._rewardCalculatorService.get_cosine_similarity_text())
        output.set_is_done(episodeHandler.is_done())

    def _get_percent(self, ratio):
        return ratio * 100
