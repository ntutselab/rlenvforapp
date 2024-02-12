from RLEnvForApp.usecase.targetPage.dto.DirectiveDTO import DirectiveDTO


class CreateDirectiveOutput:
    def __init__(self):
        self._isLegalDirective = False
        self._directiveDTO: DirectiveDTO = None
        self._lastDom = ""

    def set_is_legal_directive(self, isLegalDirective: bool):
        self._isLegalDirective = isLegalDirective

    def set_directive_dto(self, directiveDTO: DirectiveDTO):
        self._directiveDTO = directiveDTO

    def set_last_dom(self, lastDom: str):
        self._lastDom = lastDom

    def get_is_legal_directive(self) -> bool:
        return self._isLegalDirective

    def get_directive_dto(self) -> DirectiveDTO:
        return self._directiveDTO

    def get_last_dom(self) -> str:
        return self._lastDom
