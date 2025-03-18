from RLEnvForApp.domain.environment.autOperator.IAUTOperator import IAUTOperator

from . import IActionCommand


class SelectOptionCommand(IActionCommand.IActionCommand):
    def __init__(self, optionValue: str, actionNumber: int):
        super().__init__(actionNumber=actionNumber, actionType="select")
        self._optionValue = optionValue

    def execute(self, operator: IAUTOperator):
        operator.setActionType(super().getActionType())
        operator.executeAppEvent(xpath="", value=self._optionValue)
