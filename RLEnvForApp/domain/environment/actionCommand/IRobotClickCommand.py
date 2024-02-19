from RLEnvForApp.domain.environment.autOperator.IAUTOperator import IAUTOperator

from . import IActionCommand


class IRobotClickCommand(IActionCommand.IActionCommand):
    def __init__(self, actionNumber: int):
        super().__init__(actionNumber=actionNumber, actionType="click")

    def execute(self, operator: IAUTOperator):
        operator.setActionType(super().getActionType())
        operator.setActionNumber(super().getActionNumber())
        operator.executeAppEvent(xpath="", value="")
        operator.changeFocus()
