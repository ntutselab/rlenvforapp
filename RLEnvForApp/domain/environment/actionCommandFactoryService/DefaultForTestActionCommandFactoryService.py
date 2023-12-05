from RLEnvForApp.domain.environment.actionCommandFactoryService import IActionCommandFactoryService
from RLEnvForApp.domain.environment.actionCommand import *

# 0. submit
# 1. change focus
# 2. abc@gmail.com
# 3. 10
# 4. 2020/05/29
# 5. sgfsdg
# 6. 0984000000
# 7. Michael Chen

class DefaultForTestActionCommandFactoryService(IActionCommandFactoryService.IActionCommandFactoryService):
    def __init__(self):
        super().__init__()
        self._inputData = ["abc@gmail.com", "10", "2020/05/29", "sgfsdg", "0984000000", "Michael Chen"]
        self._inputActionStartNumber = 2

    def createActionCommand(self, actionNumber: int) -> IActionCommand:

        if actionNumber == 0:
            return ClickCommand.ClickCommand(actionNumber=actionNumber)

        if actionNumber == 1:
            return ChangeFocusCommand.ChangeFocusCommand(actionNumber=actionNumber)

        if actionNumber >= 0 and actionNumber < self.getActionSpaceSize():
            indexOfInputData = actionNumber - self._inputActionStartNumber
            return InputValueCommand.InputValueCommand(inputValue=self._inputData[indexOfInputData], actionNumber=actionNumber)

    def getActionSpaceSize(self) -> int:
        return self._inputActionStartNumber + len(self._inputData)
