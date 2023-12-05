class ITargetPagePort:
    def __init__(self):
        pass

    def connect(self):
        pass

    def close(self):
        pass

    def waitForTargetPage(self):
        pass

    def pullTargetPage(self):
        pass

    def pushTargetPage(self, targetPageId: str, episodeHandlerId: str):
        pass

    def getPauseAgent(self):
        pass

    def setPauseAgent(self, isPauseAgent: bool):
        pass
