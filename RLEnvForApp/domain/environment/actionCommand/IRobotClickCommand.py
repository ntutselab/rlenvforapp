from RLEnvForApp.domain.environment.autOperator.IAUTOperator import \
    IAUTOperator

from . import IActionCommand


class IRobotClickCommand(IActionCommand.IActionCommand):
    def __init__(self, actionNumber: int):
        super().__init__(actionNumber=actionNumber, action_type="click")

    def execute(self, operator: IAUTOperator):
        operator.set_action_type(super().get_action_type())
        operator.set_action_number(super().get_action_number())
        operator.execute_app_event(xpath="", value="")
        operator.change_focus()
