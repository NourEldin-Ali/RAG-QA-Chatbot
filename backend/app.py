
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
from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel

load_dotenv()

# Load environment variables
openai_key = os.getenv("OPENAI_KEY")
llm_based_url = os.getenv("LLM_BASE_URL")
model_name = os.getenv("MODEL_NAME")
temperature = os.getenv("TEMPERATURE")

# Load llm
llm_connector = LLMConnector(model_name,
                        temperature=temperature,
                        llm_type=LLMType.OLLAMA if openai_key is None or openai_key ==""  else LLMType.OPEN_AI,
                        server_key=openai_key,
                        base_url=llm_based_url)
llm_model = llm_connector()

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

# Create a DBController
db_controller = DBController(vector_db=vector_db)
# create a LLMController
llm_controller = LLMController(llm_model=llm_model, vector_db=vector_db, k=2)


# Initialize FastAPI app
app = FastAPI()

class QueryRequest(BaseModel):
    query: str

@app.post("/query")
def query_llm(request: QueryRequest):
    """Endpoint to send a query and get a response."""
    if not request.query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    response = llm_controller.get_responce(request.query)
    return {"result": response["result"]}

@app.get("/delete-collection")
def delete_collection():
    """Endpoint to delete all documents from the collection."""
    try:
        db_controller.delete_all_documents()
        return {"message": "All documents deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/reinitialize-data")
def reinitialize_data():
    """Endpoint to reinitialize data from files and save to the database."""
    try:
        print("Reinitializing data...")
        docs_path = "docs"
        documents = read_docs(docs_path)
        db_controller.add_documents(documents)
        print("End data...")
        return {"message": "Data reinitialized successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


reinitialize_data()


# if __name__ == "__main__":
#     host = "0.0.0.0"
#     port = 5000
#     uvicorn.run(app, host=host, port=port)


# # %%
# # Load documents from a directory (e.g., "docs/")
# docs_path = "docs"
# documents = read_docs(docs_path)



# db_controller.add_documents(documents)
# # %%
# db_controller.delete_all_documents()
# # %%
# db_controller.get_all_documents()

# # %%
# # define llm controller class
# llm_controller = LLMController(llm_model=llm_model, vector_db=vector_db, k=2)

# # %%
# # Ask user for input query
# query = "what is the docker?"

# # Get response
# response = llm_controller.get_responce(query)
# print(response['result'])

