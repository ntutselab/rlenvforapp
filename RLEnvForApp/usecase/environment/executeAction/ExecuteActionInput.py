from RLEnvForApp.domain.formInput.textGeneration.ITextGenerationService import ITextGenerationService
class ExecuteActionInput:
    def __init__(self, actionNumber: int, episodeHandlerId: str, aut_name: str, url: str, xpath: str, prompt: str, try_count: int, is_element_in_feedback: bool, textGenerationService: ITextGenerationService):
        self._actionNumber = actionNumber
        self._episodeHandlerId = episodeHandlerId
        self._aut_name = aut_name
        self._url = url
        self._xpath = xpath
        self._prompt = prompt
        self._try_count = try_count
        self.__is_element_in_feedback= False
        self._textGenerationService = textGenerationService

    def getActionNumber(self):
        return self._actionNumber

    def getEpisodeHandlerId(self):
        return self._episodeHandlerId

    def getAutName(self):
        return self._aut_name

    def getUrl(self):
        return self._url

    def getXpath(self):
        return self._xpath
    
    def getPrompt(self):
        return self._prompt
    
    def getTextGenerationService(self):
        return self._textGenerationService
    
    def getTryCount(self):
        return self._try_count
    
    def getIsElementInFeedback(self):
        return self.__is_element_in_feedback