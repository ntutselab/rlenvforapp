from RLEnvForApp.domain.environment.episodeHandler.IEpisodeHandler import \
    IEpisodeHandler
from RLEnvForApp.domain.environment.rewardCalculatorService.ActionIndicationService.IActionIndicationService import \
    IActionIndicationService
from RLEnvForApp.domain.environment.rewardCalculatorService.IRewardCalculatorService import \
    IRewardCalculatorService
from RLEnvForApp.domain.environment.state.State import State
from RLEnvForApp.domain.targetPage.TargetIndicationService.ITargetIndicationService import \
    ITargetIndicationService
from RLEnvForApp.usecase.environment.executeAction.ActionIndicationService.CheckHTMLLogActionIndicationService import \
    CheckHTMLLogActionIndicationService
from RLEnvForApp.usecase.targetPage.ITargetIndicationService.HTMLLogIndicationService import \
    HTMLLogIndicationService


class AIGuideHTMLLogRewardCalculatorService(IRewardCalculatorService):
    def __init__(self):
        super().__init__()
        self._step_reward_coefficient = 1
        self._episode_reward_coefficient = 1000
        self._target_indication_service: ITargetIndicationService = HTMLLogIndicationService()
        self._action_indication_service: IActionIndicationService = CheckHTMLLogActionIndicationService()

    def calculate_reward(self, episode_handler: IEpisodeHandler):
        state: State = episode_handler.get_state(
            index=episode_handler.get_number_of_state() - 1)
        episode_step_fraction = self._get_episode_step_fraction(
            episode_handler=episode_handler)

        if episode_handler.is_done() and self._target_indication_service.is_conform(state=state):
            return self._episode_reward_coefficient * (1 / episode_step_fraction)

        if self._action_indication_service.is_conform(state=state):
            return 1
        else:
            return -1

    def _get_episode_step_fraction(self, episode_handler: IEpisodeHandler):
        episode_step_fraction = 0

        number_of_state = episode_handler.get_number_of_state()
        episode_step = episode_handler.get_episode_step()
        episode_step_fraction = (number_of_state - 1) / episode_step
        return episode_step_fraction
