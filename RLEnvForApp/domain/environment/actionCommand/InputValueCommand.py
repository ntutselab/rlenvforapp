from RLEnvForApp.domain.environment.autOperator.IAUTOperator import \
    IAUTOperator

from . import IActionCommand


class InputValueCommand(IActionCommand.IActionCommand):
    def __init__(self, inputValue: str, actionNumber: int):
        super().__init__(actionNumber=actionNumber, actionType="input")
        self._inputValue = inputValue

    def execute(self, operator: IAUTOperator):
        operator.setActionType(super().getActionType())
        operator.executeAppEvent(xpath="", value=self._inputValue)
