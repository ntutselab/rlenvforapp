from RLEnvForApp.domain.targetPage.TargetPage import TargetPage


class TargetPageProcessingManagerSingleton:
    _instance = None

    @staticmethod
    def getInstance():
        if TargetPageProcessingManagerSingleton._instance == None:
            TargetPageProcessingManagerSingleton._instance = TargetPageProcessingManagerSingleton()
        return TargetPageProcessingManagerSingleton._instance

    def __init__(self):
        if TargetPageProcessingManagerSingleton._instance != None:
            raise Exception('only one instance can exist')
        else:
            self._beProcessedTargetPage: TargetPage = None

    def setBeProcessedTargetPage(self, targetPage: TargetPage):
        self._beProcessedTargetPage = targetPage

    def getBeProcessedTargetPage(self) -> TargetPage:
        return self._beProcessedTargetPage