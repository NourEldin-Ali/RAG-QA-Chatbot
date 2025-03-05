from src.enums.db_type import DBType
from langchain_openai import ChatOpenAI
from chromadb.config import Settings
from langchain.vectorstores import Chroma

class DBConnector:
    """
    Connector for vector database such as ChromaDB.

    Attributes:
        embedding_model (object): The embedding model to be used.
        collection_name (str): The name of the collection in the database. Default is "collection".
        server_host (str): The host of the server. Default is "localhost".
        server_port (int): The port of the server. Default is 8000.
        db_type (DBType): The type of database to be used. Default is DBType.CHROMA.
    """
    def __init__(self, 
                 embedding_model: object, 
                 collection_name: str = "collection", 
                 server_host:str ="localhost", 
                 server_port:int=8000,  
                 db_type: DBType = DBType.CHROMA
                 ):
        self.embedding_model = embedding_model
        self.collection_name = collection_name
        self.server_host = server_host
        self.server_port = server_port
        self.db_type = db_type

    
    def __call__(self) -> object:
        if not self.embedding_model:
            raise ValueError("Embedding model is not defined")

        if self.db_type == DBType.CHROMA:
            return self.get_chroma_db()
        
        raise ValueError("Database type is not defined")
    
    def get_chroma_db(self) -> object:
        # ChromaDB settings to connect to the server
        client_settings = Settings(
            chroma_api_impl="chromadb.api.fastapi.FastAPI",
            chroma_server_host=self.server_host, 
            chroma_server_http_port=self.server_port
        )
        # Connect to ChromaDB running in server
        vector_db = Chroma(
            collection_name=self.collection_name,
            embedding_function=self.embedding_model,
            client_settings=client_settings
        )

        return vector_db
    
   