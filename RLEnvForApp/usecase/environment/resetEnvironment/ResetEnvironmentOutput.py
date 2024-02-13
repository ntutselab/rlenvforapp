class ResetEnvironmentOutput:
    def __init__(self):
        self._observation: [int] = []
        self._episode_handler_id = ""
        self._target_page_url = ""
        self._target_page_id = ""
        self._form_x_path = ""
        self._original_observation = {}

    def set_observation(self, observation):
        self._observation = observation

    def get_observation(self):
        return self._observation

    def set_original_observation(self, originalObservation: dict):
        self._original_observation = originalObservation

    def get_original_observation(self):
        return self._original_observation

    def set_target_page_url(self, url: str):
        self._target_page_url = url

    def get_target_page_url(self):
        return self._target_page_url

    def set_target_page_id(self, id: str):
        self._target_page_id = id

    def get_target_page_id(self):
        return self._target_page_id

    def get_form_x_path(self):
        return self._form_x_path

    def set_form_x_path(self, form_x_path: str):
        self._form_x_path = form_x_path

    def set_episode_handler_id(self, id: str):
        self._episode_handler_id = id

    def get_episode_handler_id(self):
        return self._episode_handler_id
