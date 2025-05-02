from RLEnvForApp.domain.formInput.textGeneration.ITextGenerationService import ITextGenerationService
from RLEnvForApp.domain.llmService.SystemPromptFactory import SystemPromptFactory
from RLEnvForApp.domain.llmService import LlmServiceContainer

class MixedTextGenerationService(ITextGenerationService):
    def __init__(self):
        super().__init__()
        
    def get_form_input(self, prompt: str, try_count: int = 0, is_element_in_feedback: bool = False):
        system_prompt = None
        if try_count <= 3 and not is_element_in_feedback:
            system_prompt =  SystemPromptFactory.get("select_data_faker")
        else:
            system_prompt =  SystemPromptFactory.get("get_input_value")

        llm_service = LlmServiceContainer.llm_service_instance
        response = llm_service.get_response(prompt, system_prompt) 
        if response is None:
            print("LLM response is None")
            return ""
        else:
            print(f"LLM response: {response}")
            return response