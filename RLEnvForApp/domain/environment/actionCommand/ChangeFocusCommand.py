from RLEnvForApp.domain.environment.autOperator.IAUTOperator import \
    IAUTOperator

from . import IActionCommand


class ChangeFocusCommand(IActionCommand.IActionCommand):
    def __init__(self, actionNumber: int):
        super().__init__(actionNumber=actionNumber, action_type="changeFocus")

    def execute(self, operator: IAUTOperator):
        operator.set_action_type(super().get_action_type())
        operator.change_focus()
