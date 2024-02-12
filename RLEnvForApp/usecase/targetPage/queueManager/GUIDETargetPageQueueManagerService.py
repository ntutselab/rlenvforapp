from RLEnvForApp.domain.targetPage.TargetPage import TargetPage
from RLEnvForApp.usecase.repository.TargetPageRepository import \
    TargetPageRepository
from RLEnvForApp.usecase.targetPage.mapper import TargetPageEntityMapper
from RLEnvForApp.usecase.targetPage.queueManager.ITargetPageQueueManagerService import \
    ITargetPageQueueManagerService


class GUIDETargetPageQueueManagerService(ITargetPageQueueManagerService):
    def __init__(self, repository: TargetPageRepository):
        super().__init__(repository)

    def dequeue_target_page(self) -> TargetPage:
        targetPage: TargetPage = None
        if not super().is_empty():
            targetPageEntity = super().get_repository().find_all()[0]
            targetPage = TargetPageEntityMapper.mapping_target_page_from(
                targetPageEntity=targetPageEntity)
            super().get_repository().delete_by_id(targetPage.get_id())
            self.enqueue_target_page(targetPage=targetPage)
        return targetPage

    def enqueue_target_page(self, targetPage: TargetPage):
        targetPageEntity = TargetPageEntityMapper.mapping_target_page_entity_from(
            targetPage=targetPage)
        super().get_repository().add(targetPageEntity=targetPageEntity)
