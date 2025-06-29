from faker import Faker
from RLEnvForApp.domain.formInput.textGeneration.ITextGenerationService import ITextGenerationService
from RLEnvForApp.domain.llmService.SystemPromptFactory import SystemPromptFactory
from RLEnvForApp.domain.llmService import LlmServiceContainer

class MixedTextGenerationService(ITextGenerationService):
    def __init__(self):
        super().__init__()
        
    def get_form_input(self, prompt: str, try_count: int = 0, is_element_in_feedback: bool = False):
        system_prompt = None
        is_select_data_faker_prompt = False
        if try_count <= 3 and not is_element_in_feedback:
            system_prompt =  SystemPromptFactory.get("select_data_faker")
            is_select_data_faker_prompt = True
        else:
            system_prompt =  SystemPromptFactory.get("get_input_value")
            is_select_data_faker_prompt = False

        llm_service = LlmServiceContainer.llm_service_instance
        response = llm_service.get_response(prompt, system_prompt) 
        if response is None:
            print("LLM response is None")
            return ""
        else:
            if is_select_data_faker_prompt:
                print("Using select_data_faker system prompt")
                try:
                    faker = Faker()
                    response_text = getattr(faker, response)()
                    return str(response_text)
                except AttributeError as e:
                    # 如果無法解析為 Faker 函數，則返回原始響應
                    print(f"Error parsing LLM response: {e}. Response was: {response}, It may not be a faker function")
                    return response
            
            return response
