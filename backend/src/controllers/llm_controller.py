from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
from langchain.chains import RetrievalQA

class LLMController:
    def __init__(self,llm_model, vector_db, k:int = 2):
        custom_prompt = PromptTemplate(
            input_variables=["context", "question"],
            template=(
                "You are an AI assistant. Use the following context to answer the question strictly based on the given information.\n"
                # "If the context does not explicitly contain the answer, or if the information is only related but not exact, simply respond with:\n"
                # "'I don't know the answer to that based on the provided context.'\n\n"
                # "Additionally, consider that the user may have made a typographical or input error. If the intended meaning is reasonably clear, adjust accordingly while maintaining accuracy to the context.\n\n"
                "Context:\n{context}\n\n"
                "Question: {question}\n\n"
                "Answer:"
            )
        )
        # Create a Question-Answering Chain with proper structure
        qa_chain = load_qa_chain(llm_model,
                                chain_type="stuff", prompt=custom_prompt)
        # Wrap the retriever and chain inside RetrievalQA
        self.chain = RetrievalQA(
            retriever=vector_db.as_retriever(search_kwargs={"k": k}),
            combine_documents_chain=qa_chain)

    def get_responce(self, query:str):
        response = self.chain.invoke({"query": query})
        return response