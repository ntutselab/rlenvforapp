import json
import os
import random

from RLEnvForApp.domain.environment import inputSpace
from RLEnvForApp.domain.environment.actionCommand import (
    IRobotClickCommand, IRobotInputValueCommand)
from RLEnvForApp.domain.environment.actionCommand.IActionCommand import \
    IActionCommand
from RLEnvForApp.domain.environment.actionCommandFactoryService.IActionCommandFactoryService import \
    IActionCommandFactoryService
from RLEnvForApp.domain.environment.inputSpace import ValueWeightSingleton
from RLEnvForApp.logger.logger import Logger


class CosineSimilarityActionCommandFactory(IActionCommandFactoryService):
    def __init__(self):
        super().__init__()
        self._input_data = inputSpace.inputValues

        if os.path.exists('input_value_probability.json'):
            with open('input_value_probability.json', encoding='utf-8') as jsonfile:
                data = json.load(jsonfile)
            self._inputValueWeights = data['weights']
        else:
            self._inputValueWeights = ValueWeightSingleton.get_instance().get_value_weights()

    def create_action_command(self, actionNumber: int) -> IActionCommand:
        if actionNumber == 0:
            return IRobotClickCommand.IRobotClickCommand(
                actionNumber=actionNumber)
        else:
            inputValue = random.choices(self._input_data[actionNumber],
                                        weights=self._inputValueWeights[inputSpace.inputTypes[actionNumber]], k=1)[0]
            Logger().info(f"Input value: {inputValue}")
            return IRobotInputValueCommand.IRobotInputValueCommand(
                inputValue=inputValue, actionNumber=actionNumber)

    def get_action_space_size(self) -> int:
        return len(self._input_data)

    def get_action_list(self) -> [str]:
        return self._input_data
