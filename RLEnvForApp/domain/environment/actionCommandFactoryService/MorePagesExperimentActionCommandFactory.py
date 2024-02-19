from RLEnvForApp.domain.environment.actionCommand import (ChangeFocusCommand, IRobotClickCommand,
                                                          IRobotInputValueCommand)
from RLEnvForApp.domain.environment.actionCommand.IActionCommand import IActionCommand
from RLEnvForApp.domain.environment.actionCommandFactoryService.IActionCommandFactoryService import \
    IActionCommandFactoryService

# 0. submit
# 1. change focus
inputData_2 = "vector@selab.com"
inputData_3 = "10"
# inputData_4 = "password"
inputData_4 = "selab1623"
inputData_5 = "sgfsdg"
inputData_6 = "2020/05/29"
inputData_7 = "Kai Huang"
# inputData_6 = "password"
# ClickForAllElementRewardCalculatorService


class MorePagesExperimentActionCommandFactory(IActionCommandFactoryService):
    def __init__(self):
        super().__init__()
        self._inputData = [inputData_2, inputData_3, inputData_4, inputData_5, inputData_6, inputData_7]

    def createActionCommand(self, actionNumber: int) -> IActionCommand:
        inputActionStartNumber = 2

        if actionNumber == 0:
            return IRobotClickCommand.IRobotClickCommand(actionNumber=actionNumber)

        if actionNumber == 1:
            return ChangeFocusCommand.ChangeFocusCommand(actionNumber=actionNumber)

        if actionNumber >= 0 and actionNumber < len(self._inputData) + inputActionStartNumber:
            indexOfInputData = actionNumber - inputActionStartNumber
            return IRobotInputValueCommand.IRobotInputValueCommand(inputValue=self._inputData[indexOfInputData], actionNumber=actionNumber)


    def getActionSpaceSize(self)->int:
        return 2 + len(self._inputData)

    def getActionList(self) -> [str]:
        return self._inputData
