from RLEnvForApp.domain.targetPage.TargetPage import TargetPage
from RLEnvForApp.usecase.repository.TargetPageRepository import TargetPageRepository


class ITargetPageQueueManagerService:
    def __init__(self, repository: TargetPageRepository):
        self._repository = repository

    def getRepository(self):
        return self._repository

    def isEmpty(self):
        return len(self._repository.findAll()) == 0

    def dequeueTargetPage(self) -> TargetPage:
        pass

    def enqueueTargetPage(self, targetPage: TargetPage):
        pass
