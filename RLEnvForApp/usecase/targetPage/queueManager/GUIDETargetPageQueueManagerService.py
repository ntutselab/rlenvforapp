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
        target_page: TargetPage = None
        if not super().is_empty():
            target_page_entity = super().get_repository().find_all()[0]
            target_page = TargetPageEntityMapper.mapping_target_page_from(
                target_page_entity=target_page_entity)
            super().get_repository().delete_by_id(target_page.get_id())
            self.enqueue_target_page(target_page=target_page)
        return target_page

    def enqueue_target_page(self, target_page: TargetPage):
        target_page_entity = TargetPageEntityMapper.mapping_target_page_entity_from(
            target_page=target_page)
        super().get_repository().add(target_page_entity=target_page_entity)
