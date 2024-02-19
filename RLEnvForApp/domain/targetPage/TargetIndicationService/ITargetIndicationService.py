from RLEnvForApp.domain.environment.state.State import State


class ITargetIndicationService:
    def __init__(self):
        self._a = 0
        pass

    def isConform(self, state: State) -> bool:
        pass
