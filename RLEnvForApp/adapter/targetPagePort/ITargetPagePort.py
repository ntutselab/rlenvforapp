class ITargetPagePort:
    def __init__(self):
        pass

    def connect(self):
        pass

    def close(self):
        pass

    def wait_for_target_page(self):
        pass

    def pull_target_page(self):
        pass

    def push_target_page(self, targetPageId: str, episodeHandlerId: str):
        pass

    def get_pause_agent(self):
        pass

    def set_pause_agent(self, isPauseAgent: bool):
        pass
