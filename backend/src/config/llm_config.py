from src.enums.llm_type import LLMType
from langchain_openai import ChatOpenAI
from langchain_ollama.chat_models import ChatOllama
from langchain.embeddings import OllamaEmbeddings
from langchain_openai import OpenAIEmbeddings

class LLMConnector:
    """
    Connector for various language models (LLMs) such as OpenAI GPT and Ollama.

    Attributes:
        model (object): The language model to be used.
        temperature (float): The creativity level of the model. Default is 0.0.
        api_key (str): The API key for OpenAI. Default is None.
        llm_type (LLMType): The type of language model to be used. Default is LLMType.OLLAMA.
    """
    def __init__(self, model_name: object, temperature: float = 0.0, llm_type: LLMType = LLMType.OLLAMA, server_key: str = None, base_url: str = None):
        self.model = model_name
        self.temperature = temperature
        self.llm_type = llm_type
        self.server_key = server_key
        self.base_url = base_url
    
    def __call__(self) -> object:
        if not self.model:
            raise ValueError("Model is not defined")

        if self.llm_type == LLMType.OPEN_AI:
            return self.get_openai_llm()
        else:
            return self.get_ollama_llm()
    
    def get_openai_llm(self) -> object:
        return ChatOpenAI(
            model_name=self.model,
            openai_api_key=self.server_key,
            temperature=self.temperature,
        )
    
    def get_ollama_llm(self) -> object:
        if(self.base_url is not None):
            return ChatOllama(
                model=self.model,
                temperature=self.temperature,
                base_url=self.base_url
            )
        
        return ChatOllama(
            model=self.model,
            temperature=self.temperature,
        )

    def get_embedding(self, embedding_model_name:str) -> object:
        if embedding_model_name is None:
            raise ValueError("Model is not defined")
        
        self.embedding_model_name = embedding_model_name

        if self.llm_type == LLMType.OPEN_AI:
            return OpenAIEmbeddings(model=self.embedding_model_name,
                                    api_key=self.server_key)
        else:
            if(self.base_url is not None):
                return OllamaEmbeddings(model=self.embedding_model_name, base_url=self.base_url)
            return OllamaEmbeddings(model=self.embedding_model_name)