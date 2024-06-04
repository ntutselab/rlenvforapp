from RLEnvForApp.domain.environment.state import State


class IEpisodeHandler:
    def __init__(self, id: str, episodeIndex: int, episodeStep: int):
        self._id = id
        self._episodeIndex = episodeIndex
        self._episodeStep = episodeStep
        self._states: [State] = []

    def getId(self):
        return self._id

    def getEpisodeIndex(self) -> int:
        return self._episodeIndex

    def getEpisodeStep(self):
        return self._episodeStep

    def appendState(self, state: State):
        self._states.append(state)

    def getState(self, index: int) -> State:
        return self._states[index]

    def setAllState(self, state: State):
        self._states = state

    def getAllState(self) -> [State]:
        return self._states

    def isDone(self) -> bool:
        pass

    def getNumberOfState(self) -> int:
        return len(self._states)

    def reset(self):
        self._states = []

    def remain_only_index_zero_state(self):
        self._states = self._states[:1]
