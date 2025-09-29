from IPython.display import Image, display
from reflex.agent.reflex_agent import ReflexAgent
from reflex.agent.nodes import ReflexNodes
from reflex.agent.tools import PineconeRetriever

from reflex.utils.config import get_agent_config

from reflex.api.api import FastAPIendpoint
from chainlit.utils import mount_chainlit
  


config = get_agent_config()

nodes = ReflexNodes(generate_prompt=config.generate.generate_prompt, decide_prompt=config.generate.decide_prompt)
retriever = PineconeRetriever(
    top_k=config.retriever.top_k,
    pinecone_api_key=config.retriever.pinecone_api_key,
    index_name=config.retriever.index_name)
agent = ReflexAgent(nodes=nodes, retriever = retriever, openai_api_key=config.generate.openai_api_key, temperature=config.generate.temperature, model_name=config.generate.model_name)

# try:
#     # Get the PNG data
#     png_data = agent.graph.get_graph().draw_mermaid_png()
    
#     # Save to file
#     with open('./reflex_graph.png', 'wb') as f:
#         f.write(png_data)
    
# except Exception as e:
#     raise(e)

fastapi_app = FastAPIendpoint(agent=agent).app

mount_chainlit(app=fastapi_app, target="./reflex/front/cl_entrypoint.py", path="/interface")

