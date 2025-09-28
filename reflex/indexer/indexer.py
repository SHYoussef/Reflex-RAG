from reflex.indexer.retrieval import PineconeIndexCreator, IndexCreator
from reflex.indexer.preprocessing import DocsPreprocessor


class Indexer:
    """
    Orchestrate the document preprocessing and index creation.
    """
    def __init__(self, preprocessor: DocsPreprocessor, index_creator: IndexCreator) -> None:
        self.preprocessor = preprocessor
        self.index_creator = index_creator

    def run(self) -> None:
        """Runs the full indexing pipeline."""
        # Load and preprocess documents
        docs_pages = self.preprocessor.load_documents()
        chunks = self.preprocessor.split_documents(docs_pages)
        texts = [chunk.page_content for chunk in chunks]

        # Create index and insert embeddings
        self.index_creator.create_embeddings(texts)
