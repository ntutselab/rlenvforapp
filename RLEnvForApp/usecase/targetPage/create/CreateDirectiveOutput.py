from RLEnvForApp.usecase.targetPage.dto.DirectiveDTO import DirectiveDTO


class CreateDirectiveOutput:
    def __init__(self):
        self._is_legal_directive = False
        self._directive_dto: DirectiveDTO = None
        self._last_dom = ""

    def set_is_legal_directive(self, is_legal_directive: bool):
        self._is_legal_directive = is_legal_directive

    def set_directive_dto(self, directive_dto: DirectiveDTO):
        self._directive_dto = directive_dto

    def set_last_dom(self, lastDom: str):
        self._last_dom = lastDom

    def get_is_legal_directive(self) -> bool:
        return self._is_legal_directive

    def get_directive_dto(self) -> DirectiveDTO:
        return self._directive_dto

    def get_last_dom(self) -> str:
        return self._last_dom
