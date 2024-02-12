from RLEnvForApp.domain.environment.autOperator.IAUTOperator import \
    IAUTOperator

from . import IActionCommand


class ClickCommand(IActionCommand.IActionCommand):
    def __init__(self, actionNumber: int):
        super().__init__(actionNumber=actionNumber, actionType="click")

    def execute(self, operator: IAUTOperator):
        operator.set_action_type(super().get_action_type())
        operator.execute_app_event(xpath="", value="")
