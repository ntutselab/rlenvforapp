class ITextGenerationService:
    """
    Interface for Form Input Text Service
    """
    def __init__(self):
        pass
    def get_form_input(self, prompt: str, try_count: int = 0, is_element_in_feedback: bool = False):
        pass