from RLEnvForApp.domain.targetPage.TargetPage import TargetPage
from RLEnvForApp.usecase.repository.TargetPageRepository import \
    TargetPageRepository
from RLEnvForApp.usecase.targetPage.mapper import TargetPageEntityMapper
from RLEnvForApp.usecase.targetPage.queueManager.ITargetPageQueueManagerService import \
    ITargetPageQueueManagerService


class GUIDETargetPageQueueManagerService(ITargetPageQueueManagerService):
    def __init__(self, repository: TargetPageRepository):
        super().__init__(repository)

    def dequeueTargetPage(self) -> TargetPage:
        targetPage: TargetPage = None
        if not super().isEmpty():
            targetPageEntity = super().getRepository().findAll()[0]
            targetPage = TargetPageEntityMapper.mappingTargetPageFrom(
                targetPageEntity=targetPageEntity)
            super().getRepository().deleteById(targetPage.getId())
            self.enqueueTargetPage(targetPage=targetPage)
        return targetPage

    def enqueueTargetPage(self, targetPage: TargetPage):
        targetPageEntity = TargetPageEntityMapper.mappingTargetPageEntityFrom(targetPage=targetPage)
        super().getRepository().add(targetPageEntity=targetPageEntity)
