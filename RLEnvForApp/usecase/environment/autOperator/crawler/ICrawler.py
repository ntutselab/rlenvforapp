from RLEnvForApp.usecase.environment.autOperator.dto.AppElementDTO import \
    AppElementDTO


class ICrawler:
    def __init__(self):
        pass

    def goToRootPage(self):
        pass

    def reset(self, rootPath: str, formXPath: str):
        pass

    def close(self):
        pass

    def executeAppEvent(self, xpath: str, value: str):
        pass

    def changeFocus(self, xpath: str, value: str):
        pass

    def getScreenShot(self):
        pass

    def getAllSelectedAppElementsDTOs(self) -> [AppElementDTO]:
        pass

    def getDOM(self) -> str:
        pass

    def getUrl(self) -> str:
        pass
