from RLEnvForApp.domain.environment.autOperator.IAUTOperator import \
    IAUTOperator


class IActionCommand:
    def __init__(self, actionNumber: int, actionType: str):
        self._actionNumber = actionNumber
        self._actionType = actionType

    def get_action_type(self):
        return self._actionType

    def get_action_number(self):
        return self._actionNumber

    def execute(self, operator: IAUTOperator):
        pass
