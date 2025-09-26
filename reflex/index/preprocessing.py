
from langchain_text_splitters import RecursiveCharacterTextSplitter, TextSplitter
from langchain import Document
from langchain_community.document_loaders import PyPDFLoader
import os
from pathlib import Path
from typing import List, Optional, Callable
from abc import ABC, abstractmethod

class Loader(ABC):
    @abstractmethod
    def load(self, file_paths: List[str]) -> List[Document]:
        pass   

class DocumentSplitter(ABC):
    @abstractmethod
    def split(self, docs_pages: List[Document]) -> List[Document]:
        pass



class PDFLoader(Loader):
    """Class for loading PDF documents from a folder."""

    def load(self, file_paths: List[str]) -> List[Document]:
        docs_pages = []
        for file_path in file_paths:
            loader = PyPDFLoader(file_path)
            pages = loader.load()
            docs_pages.extend(pages)
        return docs_pages


class RecursiveDocumentSplitter(DocumentSplitter):
    """Class for splitting documents into chunks."""
    def __init__(self, chunk_size: int, chunk_overlap: int):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split(self, docs_pages: List[Document]) -> List[Document]:
        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap
        )
        return text_splitter.split_documents(docs_pages)

class DocsPreprocessor:
    """
    Orchestrates loading and splitting of documents for downstream processing.
    """
    def __init__(self, chunk_size: int, chunk_overlap: int, folder_path: str,
                 loader: Loader, splitter: DocumentSplitter) -> None:
        self.folder_path = folder_path
        self.loader = loader 
        self.splitter = splitter

    def load_documents(self) -> List[Document]:
        """Loads all PDF documents from the folder."""
        folder = Path(self.folder_path)
        if not folder.exists():
            raise FileNotFoundError(f"Folder {self.folder_path} does not exist")
        pdf_files = [str(folder / file) for file in os.listdir(folder) if file.endswith(".pdf")]

        return self.loader.load(pdf_files)

    def split_documents(self, docs_pages: List[Document]) -> List[Document]:
        """Splits loaded documents into chunks."""
        return self.splitter.split(docs_pages)



