from loguru import logger
from typing import List, Any
from langchain_core.retrievers import BaseRetriever
from langchain_core.documents.base import Document
from pinecone import Pinecone


class PineconeRetriever(BaseRetriever):
    # Define fields as class attributes for Pydantic
    top_k: int
    pinecone_api_key: str
    index_name: str
    fields: List[str] = ["chunk_text"]
    namespace: str = "reflex-test"
    name: str = "PineconeRetriever"
    description: str = "Use this tool to answer questions about the documents in the Pinecone index."
    pc: Any = None
    
    def __init__(self, top_k: int, pinecone_api_key: str, index_name: str) -> None:
        # Call super().__init__() first with the fields
        super().__init__(
            top_k=top_k,
            pinecone_api_key=pinecone_api_key,
            index_name=index_name
        )
        self._init_client()

    def _init_client(self) -> None:
        self.pc = Pinecone(api_key=self.pinecone_api_key)
        logger.info("Pinecone client initialized.")


    def _get_index_host_name(self) -> str:
        index_infos = self.pc.describe_index(self.index_name)
        return index_infos["host"]

    def _get_index(self) -> Pinecone.Index:
        return self.pc.Index(host=self._get_index_host_name())

    def get_relevant_documents(self, question: str) -> list[Document]:
        query = {
            "inputs": {"text": question},
            "top_k": self.top_k,
        }

        fields = self.fields
        index = self._get_index()
        results = index.search(namespace=self.namespace, query=query, fields= fields)
        return [Document(page_content=hit["fields"]["chunk_text"]) for hit in results["result"]["hits"]]


