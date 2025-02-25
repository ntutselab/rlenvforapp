from RLEnvForApp.domain.environment.episodeHandler.IEpisodeHandler import IEpisodeHandler
from RLEnvForApp.domain.environment.rewardCalculatorService.IRewardCalculatorService import \
    IRewardCalculatorService
from RLEnvForApp.domain.environment.state import AppElement, State


class DefaultForTestRewardCalculatorService(IRewardCalculatorService):
    def __init__(self):
        super().__init__()
        self._episodeDoneRewardCoefficient: float = 50
        self._changeFocusRewardCoefficient: float = -1

        self._inputRewardCoefficient: float = 3.5
        self._inputRewardBaseLine: float = -3

    def calculateReward(self, episodeHandler: IEpisodeHandler):
        reward = 0.0
        numberOfState = episodeHandler.getNumberOfState()
        lastState = episodeHandler.getState(numberOfState - 1)

        if self._isInputAction(lastState=lastState):
            reward = self._getInputValueReward(elementTagName=lastState.getInteractedElement(
            ).getName(), inputValue=lastState.getAppEventInputValue())

        if self._isChangeFocusAction(lastState=lastState):
            reward = self._getChangeFocusReward()

        if self._isClickAction(lastState=lastState):
            reward = self._getClickReward()

        if episodeHandler.isDone():
            reward = self._getEpisodeDoneReward(appElements=lastState.getAllSelectedAppElements())

        return reward

    def _isInputAction(self, lastState: State):
        return lastState.getActionType() == "input"

    def _isChangeFocusAction(self, lastState: State):
        return lastState.getActionType() == "changeFocus"

    def _isClickAction(self, lastState: State):
        return lastState.getActionType() == "click"

    def _getInputValueReward(self, elementTagName: str, inputValue: str):
        rewardRevise = 0
        if "name" in elementTagName:
            if inputValue == "Michael Chen":
                rewardRevise = self._inputRewardCoefficient * 1.0
            elif inputValue == "sgfsdg":
                rewardRevise = self._inputRewardCoefficient * 0.5
            else:
                rewardRevise = self._inputRewardCoefficient * 0.25

        if "email" in elementTagName:
            if inputValue == "abc@gmail.com":
                rewardRevise = self._inputRewardCoefficient * 1.0
            else:
                rewardRevise = self._inputRewardCoefficient * 0

        if "password" in elementTagName:
            if (inputValue == "2020/05/29") or (inputValue == "0984000000") or (inputValue == "Michael Chen"):
                rewardRevise = self._inputRewardCoefficient * 1

            if (inputValue == "sgfsdg") or (inputValue == "10"):
                rewardRevise = self._inputRewardCoefficient * 0.5

            if inputValue == "abc@gmail.com":
                rewardRevise = self._inputRewardCoefficient * 0.25

        return self._inputRewardBaseLine + rewardRevise

    def _getChangeFocusReward(self):
        return self._changeFocusRewardCoefficient

    def _getClickReward(self):
        return self._inputRewardBaseLine

    def _getEpisodeDoneReward(self, appElements: [AppElement]):
        isSuccessed = True
        password = ""
        for appElement in appElements:
            if appElement.getValue() == "":
                isSuccessed = False
            if "email" in appElement.getName():
                if appElement.getValue() != "abc@gmail.com":
                    isSuccessed = False
            if "password" in appElement.getName():
                if password == "":
                    password = appElement.getValue()
                elif password != appElement.getValue():
                    isSuccessed = False

        if isSuccessed:
            return self._episodeDoneRewardCoefficient
        else:
            return self._episodeDoneRewardCoefficient * -0.5
