from RLEnvForApp.domain.environment.episodeHandler.IEpisodeHandler import \
    IEpisodeHandler
from RLEnvForApp.domain.environment.rewardCalculatorService.ActionIndicationService.IActionIndicationService import \
    IActionIndicationService
from RLEnvForApp.domain.environment.rewardCalculatorService.IRewardCalculatorService import \
    IRewardCalculatorService
from RLEnvForApp.domain.environment.state.State import State
from RLEnvForApp.domain.targetPage.TargetIndicationService.ITargetIndicationService import \
    ITargetIndicationService
from RLEnvForApp.usecase.environment.executeAction.ActionIndicationService.CheckActionTypeIndicationService import \
    CheckActionTypeIndicationService
from RLEnvForApp.usecase.targetPage.ITargetIndicationService.GUIDEIndicationService import \
    GUIDEIndicationService


class AIGuideRewardCalculatorService(IRewardCalculatorService):
    def __init__(self):
        super().__init__()
        self._stepRewardCoefficient = 1
        self._episodeRewardCoefficient = 1000
        self._targetIndicationService: ITargetIndicationService = GUIDEIndicationService()
        self._actionIndicationService: IActionIndicationService = CheckActionTypeIndicationService()

    def calculate_reward(self, episodeHandler: IEpisodeHandler):
        state: State = episodeHandler.get_state(
            index=episodeHandler.get_number_of_state() - 1)
        episodeStepFraction = self._get_episode_step_fraction(
            episodeHandler=episodeHandler)
        if episodeHandler.is_done() and self._targetIndicationService.is_conform(state=state):
            return self._episodeRewardCoefficient * (1 / episodeStepFraction)

        if self._actionIndicationService.is_conform(state=state):
            return 1
        else:
            return -1

    def _get_episode_step_fraction(self, episodeHandler: IEpisodeHandler):
        episodeStepFraction = 0

        numberOfState = episodeHandler.get_number_of_state()
        episodeStep = episodeHandler.get_episode_step()
        episodeStepFraction = (numberOfState - 1) / episodeStep
        return episodeStepFraction
