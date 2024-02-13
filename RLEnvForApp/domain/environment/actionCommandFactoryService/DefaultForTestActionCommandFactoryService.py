from RLEnvForApp.domain.environment.actionCommand import (ChangeFocusCommand,
                                                          ClickCommand,
                                                          IActionCommand,
                                                          InputValueCommand)
from RLEnvForApp.domain.environment.actionCommandFactoryService import \
    IActionCommandFactoryService

# 0. submit
# 1. change focus
# 2. abc@gmail.com
# 3. 10
# 4. 2020/05/29
# 5. sgfsdg
# 6. 0984000000
# 7. Michael Chen


class DefaultForTestActionCommandFactoryService(
        IActionCommandFactoryService.IActionCommandFactoryService):
    def __init__(self):
        super().__init__()
        self._input_data = [
            "abc@gmail.com",
            "10",
            "2020/05/29",
            "sgfsdg",
            "0984000000",
            "Michael Chen"]
        self._input_action_start_number = 2

    def create_action_command(self, actionNumber: int) -> IActionCommand:

        if actionNumber == 0:
            return ClickCommand.ClickCommand(actionNumber=actionNumber)

        if actionNumber == 1:
            return ChangeFocusCommand.ChangeFocusCommand(
                actionNumber=actionNumber)

        if actionNumber >= 0 and actionNumber < self.get_action_space_size():
            indexOfInputData = actionNumber - self._input_action_start_number
            return InputValueCommand.InputValueCommand(
                inputValue=self._input_data[indexOfInputData], actionNumber=actionNumber)

    def get_action_space_size(self) -> int:
        return self._input_action_start_number + len(self._input_data)
