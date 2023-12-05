from RLEnvForApp.domain.environment.state.State import State
from RLEnvForApp.domain.targetPage.TargetPage import TargetPage


class ITargetIndicationService:
    def __init__(self):
        self._a = 0
        pass

    def isConform(self, state: State) -> bool:
        pass
