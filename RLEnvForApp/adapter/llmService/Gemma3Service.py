from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import Runnable

from RLEnvForApp.domain.llmService.ILlmService import ILlmService
from RLEnvForApp.domain.llmService.SystemPromptFactory import SystemPromptFactory

class Gemma3Service(ILlmService):
    llm = None
    llm_chain: Runnable = None

    DEFAULT_SYSTEM_PROMPT = SystemPromptFactory.get("filter_feedback")

    def __init__(self, model_name="gemma3:12b", temperature=0.0):
        self.llm = ChatOllama(model=model_name, temperature=temperature)
        self._set_system_prompt(self.DEFAULT_SYSTEM_PROMPT)

    def _get_llm_chain_with_system_prompt(self, system_prompt: str, *args):
        system_prompt_template = PromptTemplate.from_template(system_prompt)
        return system_prompt_template | self.llm

    def _set_system_prompt(self, system_prompt: str, *args):
        self.llm_chain = self._get_llm_chain_with_system_prompt(system_prompt, *args)

    def get_response(self, prompt: str, system_prompt: str = None, *args) -> str:
        chain = self.llm_chain
        if system_prompt:
            chain = self._get_llm_chain_with_system_prompt(system_prompt, *args)
        return chain.invoke(prompt).content
