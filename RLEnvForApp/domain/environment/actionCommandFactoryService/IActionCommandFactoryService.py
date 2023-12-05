from RLEnvForApp.domain.environment.actionCommand import IActionCommand


class IActionCommandFactoryService:
    def __init__(self):
        pass

    def createActionCommand(self, actionNumber: int) -> IActionCommand:
        pass

    def getActionSpaceSize(self) -> int:
        pass

    def getActionList(self) -> [str]:
        pass