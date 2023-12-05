from RLEnvForApp.usecase.targetPage.dto.DirectiveDTO import DirectiveDTO


class CreateDirectiveOutput:
    def __init__(self):
        self._isLegalDirective = False
        self._directiveDTO: DirectiveDTO = None
        self._lastDom = ""

    def setIsLegalDirective(self, isLegalDirective: bool):
        self._isLegalDirective = isLegalDirective

    def setDirectiveDTO(self, directiveDTO: DirectiveDTO):
        self._directiveDTO = directiveDTO

    def setLastDom(self, lastDom: str):
        self._lastDom = lastDom

    def getIsLegalDirective(self) -> bool:
        return self._isLegalDirective

    def getDirectiveDTO(self) -> DirectiveDTO:
        return self._directiveDTO

    def getLastDom(self) -> str:
        return self._lastDom
