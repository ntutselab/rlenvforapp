from RLEnvForApp.domain.targetPage.TargetPage import TargetPage
from RLEnvForApp.usecase.repository.TargetPageRepository import \
    TargetPageRepository


class ITargetPageQueueManagerService:
    def __init__(self, repository: TargetPageRepository):
        self._repository = repository

    def get_repository(self):
        return self._repository

    def is_empty(self):
        return len(self._repository.find_all()) == 0

    def dequeue_target_page(self) -> TargetPage:
        pass

    def enqueue_target_page(self, target_page: TargetPage):
        pass
