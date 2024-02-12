class ResetEnvironmentOutput:
    def __init__(self):
        self._observation: [int] = []
        self._episodeHandlerId = ""
        self._targetPageUrl = ""
        self._targetPageId = ""
        self._formXPath = ""
        self._originalObservation = {}

    def set_observation(self, observation):
        self._observation = observation

    def get_observation(self):
        return self._observation

    def set_original_observation(self, originalObservation: dict):
        self._originalObservation = originalObservation

    def get_original_observation(self):
        return self._originalObservation

    def set_target_page_url(self, url: str):
        self._targetPageUrl = url

    def get_target_page_url(self):
        return self._targetPageUrl

    def set_target_page_id(self, id: str):
        self._targetPageId = id

    def get_target_page_id(self):
        return self._targetPageId

    def get_form_x_path(self):
        return self._formXPath

    def set_form_x_path(self, formXPath: str):
        self._formXPath = formXPath

    def set_episode_handler_id(self, id: str):
        self._episodeHandlerId = id

    def get_episode_handler_id(self):
        return self._episodeHandlerId
