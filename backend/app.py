
# %% 
# Libraries
import os
from dotenv import load_dotenv
from src.utils.read_docs import read_docs
from src.config.llm_config import LLMConnector
from src.config.db_config import DBConnector
from src.enums.llm_type import LLMType
from src.controllers.db_controller import DBController
from src.controllers.llm_controller import LLMController

load_dotenv()
# %%
# Load environment variables
openai_key = os.getenv("OPENAI_KEY")
llm_based_url = os.getenv("LLM_BASE_URL")
model_name = os.getenv("MODEL_NAME")
temperature = os.getenv("TEMPERATURE")

# Load llm
llm_connector = LLMConnector(model_name,
                         temperature=temperature,
                         llm_type=LLMType.OLLAMA if openai_key is None else LLMType.OPEN_AI,
                         server_key=openai_key,
                         base_url=llm_based_url)
llm_model = llm_connector()

# %%
# Get embedding model
embedding_model_name = os.getenv("EMBEDDING_MODEL_NAME")
embedding_model = llm_connector.get_embedding(embedding_model_name)

# load environment variables
chroma_server = os.getenv("CHROMA_DB_SERVER_HOST")
chroma_port = os.getenv("CHROMA_DB_SERVER_PORT")
chroma_collection_name = os.getenv("CHROMA_DB_COLLECTION_NAME")

# Connect to the database
db_connector = DBConnector(embedding_model=embedding_model,
                           server_host=chroma_server,
                           server_port=chroma_port,
                           collection_name=chroma_collection_name)
vector_db = db_connector()

# %%
# Create a DBController
db_controller = DBController(vector_db=vector_db)


# %%
# Load documents from a directory (e.g., "docs/")
docs_path = "docs"
documents = read_docs(docs_path)

# Split long documents into smaller chunks
# text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
# chunks = text_splitter.split_documents(documents)

db_controller.add_documents(documents)
# %%
db_controller.delete_all_documents()
# %%
db_controller.get_all_documents()

# %%
# define llm controller class
llm_controller = LLMController(llm_model=llm_model, vector_db=vector_db, k=2)

# %%
# Ask user for input query
query = "You should anser me event you dont have context, what is the docker?"

# Get response
response = llm_controller.get_responce(query)
print(response['result'])

