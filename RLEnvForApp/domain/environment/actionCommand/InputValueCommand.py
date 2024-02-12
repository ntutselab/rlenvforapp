from RLEnvForApp.domain.environment.autOperator.IAUTOperator import \
    IAUTOperator

from . import IActionCommand


class InputValueCommand(IActionCommand.IActionCommand):
    def __init__(self, inputValue: str, actionNumber: int):
        super().__init__(actionNumber=actionNumber, actionType="input")
        self._inputValue = inputValue

    def execute(self, operator: IAUTOperator):
        operator.set_action_type(super().get_action_type())
        operator.execute_app_event(xpath="", value=self._inputValue)
