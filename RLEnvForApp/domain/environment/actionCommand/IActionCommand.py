from RLEnvForApp.domain.environment.autOperator.IAUTOperator import \
    IAUTOperator


class IActionCommand:
    def __init__(self, actionNumber: int, action_type: str):
        self._action_number = actionNumber
        self._action_type = action_type

    def get_action_type(self):
        return self._action_type

    def get_action_number(self):
        return self._action_number

    def execute(self, operator: IAUTOperator):
        pass
