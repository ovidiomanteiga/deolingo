
from enum import Enum

from langchain_community.llms import GPT4All
from langchain_openai.llms import OpenAI
from langchain_community.llms import HuggingFaceHub
from langchain.prompts import PromptTemplate
import google.generativeai as genai
import os


_template = """
You are a Clingo expert and a Deontic logic expert. 
Using the following theory atoms &obligatory{{}} and &forbidden{{}}.
Write a deontic logic program in Clingo based on the following description:
{text}
"""


class Generator(str, Enum):
    GEMINI = "gemini"
    GPT4ALL = "gpt4all"
    OPENAI = "openai"
    HUGGINGFACEHUB = "huggingfacehub"


class DeonticProgramGenerator:

    def __init__(self, generator=Generator.GPT4ALL):
        self._generator = generator
        self._openai_api_key = os.getenv('OPENAI_API_KEY', None)
        self._gemini_api_key = os.getenv('GEMINI_API_KEY', None)
        self._huggingfacehub_api_key = os.getenv('HUGGINGFACEHUB_API_KEY', None)

    def generate_program(self, natural_language_text):
        if self._generator == Generator.GEMINI and self._gemini_api_key is not None:
            return self._generate_program_gemini(natural_language_text)
        else:
            return self._generate_program_langchain(natural_language_text)

    def _generate_program_langchain(self, natural_language_text):
        if self._generator == Generator.OPENAI and self._openai_api_key is not None:
            llm = OpenAI(model_name="gpt-3.5-turbo-16k", temperature=0, openai_api_key=self._openai_api_key)
        elif self._generator == Generator.HUGGINGFACEHUB and self._huggingfacehub_api_key is not None:
            llm = HuggingFaceHub(model_name="gpt2", huggingfacehub_api_key=self._huggingfacehub_api_key)
        else:
            llm = GPT4All(model="./deolingo/models/mistral-7b-instruct-v0.1.Q4_0.gguf")
        prompt = PromptTemplate(input_variables=["text"], template=_template)
        chain = prompt | llm
        output = chain.invoke({"text": natural_language_text})
        return output

    def _generate_program_gemini(self, natural_language_text):
        genai.configure(api_key=self._gemini_api_key)
        model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest")
        response = model.generate_content([_template, natural_language_text])
        return response

