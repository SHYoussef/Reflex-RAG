from reflex.indexer.indexer import Indexer
from reflex.indexer.preprocessing import DocsPreprocessor, PDFLoader, RecursiveDocumentSplitter
from reflex.indexer.index import PineconeIndexCreator
from reflex.utils.config import get_indexer_config

def main():
    # Initialize configuration
    config = get_indexer_config()
    # Initialize the document preprocessor
    folder_path = config.preprocessor.folder_path
    loader = PDFLoader()
    splitter = RecursiveDocumentSplitter(
        chunk_size=config.preprocessor.chunk_size,
        chunk_overlap=config.preprocessor.chunk_overlap
    )
    preprocessor = DocsPreprocessor(folder_path=folder_path, loader=loader, splitter=splitter)

    # Initialize the Pinecone index creator
    index_name = config.index.index_name
    pinecone_api_key = config.index.pinecone_api_key
    region = config.index.region
    model = config.index.model  
    index_creator = PineconeIndexCreator(
        index_name=index_name,
        pinecone_api_key=pinecone_api_key,
        region=region,
        model=model
    )
    # Create the indexer and run the indexing process
    indexer = Indexer(preprocessor=preprocessor, index_creator=index_creator)
    indexer.run()


if __name__ == "__main__":
    main()