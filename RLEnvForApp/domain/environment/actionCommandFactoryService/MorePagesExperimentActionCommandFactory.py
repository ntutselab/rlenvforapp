from RLEnvForApp.domain.environment.actionCommand import (
    ChangeFocusCommand, IRobotClickCommand, IRobotInputValueCommand)
from RLEnvForApp.domain.environment.actionCommand.IActionCommand import \
    IActionCommand
from RLEnvForApp.domain.environment.actionCommandFactoryService.IActionCommandFactoryService import \
    IActionCommandFactoryService

# 0. submit
# 1. change focus
INPUT_DATA_2 = "vector@selab.com"
INPUT_DATA_3 = "10"
# inputData_4 = "password"
INPUT_DATA_4 = "selab1623"
INPUT_DATA_5 = "sgfsdg"
INPUT_DATA_6 = "2020/05/29"
INPUT_DATA_7 = "Kai Huang"
# inputData_6 = "password"
# ClickForAllElementRewardCalculatorService


class MorePagesExperimentActionCommandFactory(IActionCommandFactoryService):
    def __init__(self):
        super().__init__()
        self._input_data = [
            INPUT_DATA_2,
            INPUT_DATA_3,
            INPUT_DATA_4,
            INPUT_DATA_5,
            INPUT_DATA_6,
            INPUT_DATA_7]

    def create_action_command(self, actionNumber: int) -> IActionCommand:
        input_action_start_number = 2

        if actionNumber == 0:
            return IRobotClickCommand.IRobotClickCommand(
                actionNumber=actionNumber)

        if actionNumber == 1:
            return ChangeFocusCommand.ChangeFocusCommand(
                actionNumber=actionNumber)

        if actionNumber >= 0 and actionNumber < len(
                self._input_data) + input_action_start_number:
            indexOfInputData = actionNumber - input_action_start_number
            return IRobotInputValueCommand.IRobotInputValueCommand(
                inputValue=self._input_data[indexOfInputData], actionNumber=actionNumber)

    def get_action_space_size(self) -> int:
        return 2 + len(self._input_data)

    def get_action_list(self) -> [str]:
        return self._input_data
