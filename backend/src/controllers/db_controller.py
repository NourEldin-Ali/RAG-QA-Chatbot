from src.config.db_config import DBConnector
from src.enums.db_type import DBType


class DBController:
    def __init__(self,
                  vector_db: object):
        
        self.vector_db = vector_db
        
    def add_documents(self, documents:list):
        from uuid import uuid4
    
        # Retrieve existing documents
        existing_docs = self.get_all_documents()

        # Extract sources from existing documents
        existing_sources = {doc["source"] for doc in existing_docs["metadatas"]}

        new_documents = []

        for doc in documents:
            if doc.metadata["source"] not in existing_sources:  # Check if source exists
                new_documents.append(doc)

        if new_documents:
            uuids = [str(uuid4()) for _ in range(len(new_documents))]
            return self.vector_db.add_documents(documents=new_documents, ids=uuids)



        return "No new documents to add."

    def update_documents(self, documents: list, uuids):
        return self.vector_db.update_documents(ids=uuids, 
                                                documents=documents)
    
    def delete_documents(self, uuids):
        return self.vector_db.delete(ids=uuids)
    
    def  delete_all_documents(self):
        return self.vector_db.delete_collection()
    
    def get_all_documents(self):
        return self.vector_db.get()
    
    def search_documents(self, query: str, top_k: int = 2):
        return self.vector_db.similarity_search(query,
                                                k=top_k,
                                                # filter={"source": "tweet"}, # Optional, if you want to filter the search
                                                )