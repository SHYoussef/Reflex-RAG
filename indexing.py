from reflex.indexer.indexer import Indexer
from reflex.indexer.preprocessing import DocsPreprocessor
from reflex.indexer.retrieval import PineconeIndexCreator
from reflex.utils.config import get_index_config

def main():
    # Initialize configuration
    config = get_index_config()

    # Initialize the document preprocessor
    folder_path = config.folder_path
    preprocessor = DocsPreprocessor(folder_path=folder_path)

    # Initialize the Pinecone index creator
    index_name = config.index_name
    pinecone_api_key = config.pinecone_api_key
    region = config.region 
    model = config.model  
    index_creator = PineconeIndexCreator(
        index_name=index_name,
        pinecone_api_key=pinecone_api_key,
        region=region,
        model=model
    )
    # Create the indexer and run the indexing process
    indexer = Indexer(preprocessor=preprocessor, index_creator=index_creator)
    indexer.run()