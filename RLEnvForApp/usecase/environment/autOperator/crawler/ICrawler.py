from RLEnvForApp.usecase.environment.autOperator.dto.AppElementDTO import \
    AppElementDTO


class ICrawler:
    def __init__(self):
        pass

    def go_to_root_page(self):
        pass

    def reset(self, rootPath: str, formXPath: str):
        pass

    def close(self):
        pass

    def execute_app_event(self, xpath: str, value: str):
        pass

    def change_focus(self, xpath: str, value: str):
        pass

    def get_screen_shot(self):
        pass

    def get_all_selected_app_elements_dt_os(self) -> [AppElementDTO]:
        pass

    def get_dom(self) -> str:
        pass

    def get_url(self) -> str:
        pass
