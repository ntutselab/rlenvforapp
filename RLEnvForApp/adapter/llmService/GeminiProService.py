# !/usr/bin/env python3
from RLEnvForApp.domain.llmService.ILlmService import ILlmService
from langchain.prompts import PromptTemplate

# For Groq-specific models
from langchain_google_genai import ChatGoogleGenerativeAI

GOOGLE_API_KEY = "****"

class GeminiProService(ILlmService):
    llm = None
    llm_chain = None
    DEFAULT_SYSTEM_PROMPT = """<<SYS>>
    Please generate the most suitable value based on the form title, input fields, feedback, and context.
    Criterion: Generate the values that best meets the requirements of the form's input fields.
    Output format:
    Output as a python list string
    1. The order is based on the order of the given input fields
    2. Each element should have only one answer
    <</SYS>>

    [INST] 
    {prompt}
    [/INST]"""
    
    def __init__(self, model_name="	gemini-2.5-pro", temperature=0):
        print("init pro model")
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", google_api_key=GOOGLE_API_KEY, model_name=model_name)
        self._set_system_prompt(self.DEFAULT_SYSTEM_PROMPT, None, None, None)
        print("init pro model complete")
    
    def _get_llm_chain_with_system_prompt(self, system_prompt: str, *args) :
        system_prompt_template = PromptTemplate.from_template(system_prompt)
        llm_chain = system_prompt_template | self.llm
        return llm_chain

    def _set_system_prompt(self, system_prompt: str, *args):
        self.llm_chain = self._get_llm_chain_with_system_prompt(system_prompt, *args)

    def get_response(self, prompt: str, system_prompt: str=None, *args) -> str:
        llm_chain = self.llm_chain
        if system_prompt is not None:
            llm_chain = self._get_llm_chain_with_system_prompt(system_prompt, *args)
        return llm_chain.invoke(prompt).content
