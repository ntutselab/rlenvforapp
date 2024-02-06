import json
import os
import random

from RLEnvForApp.domain.environment.actionCommand import *
from RLEnvForApp.domain.environment.actionCommand.IActionCommand import IActionCommand
from RLEnvForApp.domain.environment.actionCommandFactoryService.IActionCommandFactoryService import \
    IActionCommandFactoryService
from RLEnvForApp.domain.environment import inputSpace
from RLEnvForApp.domain.environment.inputSpace import ValueWeightSingleton
from RLEnvForApp.logger.logger import Logger


class CosineSimilarityActionCommandFactory(IActionCommandFactoryService):
    def __init__(self):
        super().__init__()
        self._inputData = inputSpace.inputValues

        if os.path.exists('input_value_probability.json'):
            with open('input_value_probability.json', encoding='utf-8') as jsonfile:
                data = json.load(jsonfile)
            self._inputValueWeights = data['weights']
        else:
            self._inputValueWeights = ValueWeightSingleton.getInstance().getValueWeights()

    def createActionCommand(self, actionNumber: int) -> IActionCommand:
        if actionNumber == 0:
            return IRobotClickCommand.IRobotClickCommand(actionNumber=actionNumber)
        else:
            inputValue = random.choices(self._inputData[actionNumber],
                                        weights=self._inputValueWeights[inputSpace.inputTypes[actionNumber]], k=1)[0]
            Logger().info(f"Input value: {inputValue}")
            return IRobotInputValueCommand.IRobotInputValueCommand(
                inputValue=inputValue, actionNumber=actionNumber)

    def getActionSpaceSize(self) -> int:
        return len(self._inputData)

    def getActionList(self) -> [str]:
        return self._inputData
