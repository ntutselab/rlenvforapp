from RLEnvForApp.usecase.environment.episodeHandler.entity.EpisodeHandlerEntity import \
    EpisodeHandlerEntity


class EpisodeHandlerRepository:
    def __init__(self, sizeLimit: int):
        self._sizeLimit = sizeLimit

    def get_size_limit(self):
        return self._sizeLimit

    def add(self, episodeHandlerEntity: EpisodeHandlerEntity):
        pass

    def delete_by_id(self, id: str):
        pass

    def find_by_id(self, id: str):
        pass

    def find_all(self) -> [EpisodeHandlerEntity]:
        pass

    def update(self, episodeHandlerEntity: EpisodeHandlerEntity):
        pass
