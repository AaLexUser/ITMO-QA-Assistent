import os
from typing import Optional

from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, SecretStr
from openai import OpenAI
import tiktoken

from utils import DIR, load_config


class AIInference:

    def __init__(self, model: Optional[str] = None, base_url: Optional[str] = None, api_key: Optional[str] = None):
        try:
            config = load_config(f'{DIR}/config.json')
            headers = None
            chat_base_url = base_url if base_url else config['base_url']
            chat_model = model if model else config['model']
            chat_api_key = SecretStr(api_key or os.environ['OPENAI_TOKEN'])
            if "vsegpt" in chat_base_url:
                headers = {"X-Title": "MegaSchool"}
            self.model: ChatOpenAI = ChatOpenAI(model=chat_model,
                                                base_url=chat_base_url,
                                                api_key=chat_api_key,
                                                default_headers=headers,
                                                )
        except AttributeError as e:
            raise ValueError("OpenAI key is required") from e

    def chat_completion(
            self,
            user: str,
            system: Optional[str] = None,
            temperature: float = 0.2,
            frequency_penalty: float = 0.0,
            *,
            format_vals=None,
            structured: Optional[BaseModel] = None,
            tools: Optional[list] = None,
    ):
        if format_vals is None:
            format_vals = {}
        model = self.model.bind(
            temperature=temperature,
            frequency_penalty=frequency_penalty)
        if tools:
            model = model.bind_tools(tools)
        if structured:
            model = model.with_structured_output(structured)

        template: ChatPromptTemplate | PromptTemplate
        if system:
            template = ChatPromptTemplate(
                [('system', system), ('user', user)])
        else:
            template = PromptTemplate.from_template(
                user)

        execution_chain = template | model

        result = execution_chain.invoke(format_vals)
        return result

class OpenaiEmbeddings:
    def __init__(self, api_key: str, base_url: str = None, model: str = 'text-embedding-3-large'):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = model

        
    def num_tokens_from_string(string: str, encoding_name: str = 'cl100k_base') -> int:
        '''
        Returns the number of tokens in a text string.
        '''
        encoding = tiktoken.get_encoding(encoding_name)
        num_tokens = len(encoding.encode(string))

        return num_tokens
        
    def encode(self, input: str):
        try:
            response = self.client.embeddings.create(
                model=self.model, input=input, encoding_format='float'
            )
        except:
            len_embeddings = self.num_tokens_from_string(input)
            # if one of the inputs exceed the limit, raise error
            if len_embeddings > 8191:
                raise Exception(f'Input exceeds the limit of <{self.model}>!')
            else:
                raise Exception('Embeddings generation failed!')
            
        return response.data