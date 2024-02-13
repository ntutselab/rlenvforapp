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
    def __init__(self, aut_operator: IAUTOperator,
                 episodeHandlerRepository: EpisodeHandlerRepository = Provide[
                     EnvironmentDIContainers.episodeHandlerRepository],
                 rewardCalculatorService: IRewardCalculatorService = Provide[
                     EnvironmentDIContainers.rewardCalculatorService],
                 actionCommandFactory: IActionCommandFactoryService = Provide[
                     EnvironmentDIContainers.actionCommandFactory],
                 observationSerivce: IObservationService = Provide[EnvironmentDIContainers.observationService]):
        self._action_command_factory = actionCommandFactory
        self._aut_operator = aut_operator
        self._observation_service = observationSerivce
        self._episode_handler_repository = episodeHandlerRepository
        self._reward_calculator_service = rewardCalculatorService

    def execute(self, input: ExecuteActionInput.ExecuteActionInput,
                output: ExecuteActionOutput.ExecuteActionOutput):
        episode_handler_entity = self._episode_handler_repository.find_by_id(
            input.get_episode_handler_id())
        episode_handler = EpisodeHandlerEntityMapper.mapping_episode_handler_form(
            episode_handler_entity=episode_handler_entity)

        previous_state: State = episode_handler.get_all_state()[-1]
        previous_state.set_action_number(input.get_action_number())

        action_command: IActionCommand = self._action_command_factory.create_action_command(
            actionNumber=input.get_action_number())
        action_command.execute(operator=self._aut_operator)

        if input.get_action_number() == 0:
            previous_state.set_action_type("click")
        else:
            previous_state.set_action_type("input")
            previous_state.set_app_event_input_value(action_command.get_input_value())

        state: State = self._aut_operator.get_state()
        observation, originalObservation = self._observation_service.get_observation(
            state=state)
        state.set_original_observation(originalObservation)

        episode_handler.append_state(state=state)
        self._episode_handler_repository.update(
            EpisodeHandlerEntityMapper.mapping_episode_handler_entity_form(
                episode_handler=episode_handler))

        code_coverage_dict = {}
        for code_coverage in state.get_code_coverages():
            code_coverage_dict[code_coverage.get_code_coverage_type(
            )] = self._get_percent(code_coverage.get_ratio())
        output.set_observation(observation)
        output.set_original_observation(originalObservation)
        output.set_code_coverage_dict(code_coverage_dict=code_coverage_dict)
        output.set_reward(
            self._reward_calculator_service.calculate_reward(
                episode_handler=episode_handler))
        output.set_cosine_similarity_text(
            self._reward_calculator_service.get_cosine_similarity_text())
        output.set_is_done(episode_handler.is_done())

    def _get_percent(self, ratio):
        return ratio * 100
