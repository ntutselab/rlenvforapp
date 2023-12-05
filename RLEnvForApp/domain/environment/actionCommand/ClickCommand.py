from . import IActionCommand
from RLEnvForApp.domain.environment.autOperator.IAUTOperator import IAUTOperator


class ClickCommand(IActionCommand.IActionCommand):
    def __init__(self, actionNumber: int):
        super().__init__(actionNumber=actionNumber, actionType="click")

    def execute(self, operator: IAUTOperator):
        operator.setActionType(super().getActionType())
        operator.executeAppEvent(xpath="", value="")
