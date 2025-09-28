from pinecone import Pinecone, ServerlessSpec
from abc import ABC, abstractmethod
from tqdm import tqdm
import logging


class IndexCreator(ABC):
    def __init__(self) -> None:
        self.create_index()

    @abstractmethod
    def _create_index(self) -> None:
        pass
    @abstractmethod
    def create_embeddings(self) -> None:
        pass

from pinecone import Pinecone, ServerlessSpec

class PineconeIndexCreator(IndexCreator):
    """Class for creating a Pinecone index (Pinecone v3)."""
    def __init__(self, dimension: int, metric: str, index_name: str, pinecone_api_key: str, region: str, model: str) -> None:
        self.index_name = index_name
        self.pinecone_api_key = pinecone_api_key
        self.region = region
        self.model = model
        self._init_client()
        super().__init__()
    
    def _init_client(self) -> None:
        # v3 client initialization
        self.pc = Pinecone(api_key=self.pinecone_api_key)

    def _create_index(self) -> None:
        if not self.pc.has_index(self.index_name):
            self.pc.create_index(
                name=self.index_name,
                embed={
                    "model":self.model,
                    "field_map":{"text": "chunk_text"}
                    },    
                spec=ServerlessSpec(
                    cloud="aws",  # could also be "gcp" or "azure"
                    region=self.region
                )
            )
            logging.info("Index created successfully.")



    def create_embeddings(self, texts: list[str]) -> None:
        index = self.pc.index(self.index_name)
        index.upsert_records(
            [(str(i), {"chunk_text": text}) for i, text in enumerate(tqdm(texts))]
        )
        logging.info(f"Inserted {len(texts)} records into the index '{self.index_name}'.")

        
