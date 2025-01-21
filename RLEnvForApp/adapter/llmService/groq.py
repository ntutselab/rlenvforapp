#!/usr/bin/env python3
from RLEnvForApp.domain.llmService.ILlmService import ILlmService
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# For Groq-specific models
from langchain_groq import ChatGroq

GROQ_API_KEY="****"

class Groq(ILlmService):
    llm = None
    llm_chain = None
    DEFAULT_SYSTEM_PROMPT = """<<SYS>> 
    You are a software tester and designer eager to design test cases.
    <</SYS>> 
    
    [INST] Provide input values as CSV format to the following question in 150 words. Ensure that the answer is informative, \
            relevant, and concise.
            {question} 
    [/INST]"""
    
    def __init__(self, model_name="llama-3.3-70b-versatile", temperature=0):
        self.llm = ChatGroq(temperature=temperature, groq_api_key=GROQ_API_KEY,model_name=model_name)
        self._set_system_prompt(self.DEFAULT_SYSTEM_PROMPT, "question")

    def _set_system_prompt(self, system_prompt: str, *args):
        system_prompt_template = PromptTemplate(
            input_variables=args,
            template=system_prompt,
        )
        self.llm_chain = LLMChain(prompt=system_prompt_template, llm=self.llm)

    def get_response(self, prompt: str) -> str:
        return self.llm_chain.run(prompt)
