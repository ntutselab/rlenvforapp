from RLEnvForApp.domain.targetPage.TargetPage import TargetPage


class TargetPageProcessingManagerSingleton:
    _instance = None

    @staticmethod
    def get_instance():
        if TargetPageProcessingManagerSingleton._instance is None:
            TargetPageProcessingManagerSingleton._instance = TargetPageProcessingManagerSingleton()
        return TargetPageProcessingManagerSingleton._instance

    def __init__(self):
        if TargetPageProcessingManagerSingleton._instance is not None:
            raise Exception('only one instance can exist')
        else:
            self._beProcessedTargetPage: TargetPage = None

    def set_be_processed_target_page(self, targetPage: TargetPage):
        self._beProcessedTargetPage = targetPage

    def get_be_processed_target_page(self) -> TargetPage:
        return self._beProcessedTargetPage
