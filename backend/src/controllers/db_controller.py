from src.config.db_config import DBConnector
from src.enums.db_type import DBType


class DBController:
    def __init__(self,
                  vector_db: object):
        
        self.vector_db = vector_db
        
    def add_documents(self, documents:list):
        from uuid import uuid4

        uuids = [str(uuid4()) for _ in range(len(documents))]
        return self.vector_db.add_documents(documents=documents, ids=uuids)

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