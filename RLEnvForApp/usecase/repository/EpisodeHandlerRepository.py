from RLEnvForApp.usecase.environment.episodeHandler.entity.EpisodeHandlerEntity import \
    EpisodeHandlerEntity


class EpisodeHandlerRepository:
    def __init__(self, sizeLimit: int):
        self._size_limit = sizeLimit

    def get_size_limit(self):
        return self._size_limit

    def add(self, episode_handler_entity: EpisodeHandlerEntity):
        pass

    def delete_by_id(self, id: str):
        pass

    def find_by_id(self, id: str):
        pass

    def find_all(self) -> [EpisodeHandlerEntity]:
        pass

    def update(self, episode_handler_entity: EpisodeHandlerEntity):
        pass
