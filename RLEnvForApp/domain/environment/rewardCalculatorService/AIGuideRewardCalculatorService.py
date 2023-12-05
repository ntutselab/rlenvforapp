from RLEnvForApp.domain.environment.episodeHandler.IEpisodeHandler import IEpisodeHandler
from RLEnvForApp.domain.environment.rewardCalculatorService.IRewardCalculatorService import IRewardCalculatorService
from RLEnvForApp.domain.environment.state.State import State
from RLEnvForApp.domain.environment.rewardCalculatorService.ActionIndicationService.IActionIndicationService import IActionIndicationService
from RLEnvForApp.domain.targetPage.TargetIndicationService.ITargetIndicationService import ITargetIndicationService
from RLEnvForApp.domain.targetPage.TargetPage import TargetPage
from RLEnvForApp.usecase.environment.executeAction.ActionIndicationService.CheckActionTypeIndicationService import \
    CheckActionTypeIndicationService
from RLEnvForApp.usecase.targetPage.ITargetIndicationService.GUIDEIndicationService import GUIDEIndicationService


class AIGuideRewardCalculatorService(IRewardCalculatorService):
    def __init__(self):
        super().__init__()
        self._stepRewardCoefficient = 1
        self._episodeRewardCoefficient = 1000
        self._targetIndicationService: ITargetIndicationService = GUIDEIndicationService()
        self._actionIndicationService: IActionIndicationService = CheckActionTypeIndicationService()

    def calculateReward(self, episodeHandler: IEpisodeHandler):
        state: State = episodeHandler.getState(index=episodeHandler.getNumberOfState()-1)
        episodeStepFraction = self._getEpisodeStepFraction(episodeHandler=episodeHandler)
        if episodeHandler.isDone() and self._targetIndicationService.isConform(state=state):
            return self._episodeRewardCoefficient * (1/episodeStepFraction)

        if self._actionIndicationService.isConform(state=state):
            return 1
        else:
            return -1

    def _getEpisodeStepFraction(self, episodeHandler: IEpisodeHandler):
        episodeStepFraction = 0

        numberOfState = episodeHandler.getNumberOfState()
        episodeStep = episodeHandler.getEpisodeStep()
        episodeStepFraction = (numberOfState-1) / episodeStep
        return episodeStepFraction