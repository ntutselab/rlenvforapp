from RLEnvForApp.domain.environment.actionCommand import IActionCommand


class IActionCommandFactoryService:
    def __init__(self):
        pass

    def create_action_command(self, actionNumber: int) -> IActionCommand:
        pass

    def get_action_space_size(self) -> int:
        pass

    def get_action_list(self) -> [str]:
        pass
