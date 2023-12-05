class ExecuteActionInput:
    def __init__(self, actionNumber: int, episodeHandlerId: str):
        self._actionNumber = actionNumber
        self._episodeHandlerId = episodeHandlerId

    def getActionNumber(self):
        return self._actionNumber

    def getEpisodeHandlerId(self):
        return self._episodeHandlerId
