# from IPython.display import Image, display
# from reflex.agent.graph import ReflexAgent
# from reflex.agent.nodes import ReflexNodes

# nodes = ReflexNodes()
# reflex_agent = ReflexAgent(nodes=nodes)


# try:
#     # Get the PNG data
#     png_data = reflex_agent.graph.get_graph().draw_mermaid_png()
    
#     # Save to file
#     with open('./reflex_graph.png', 'wb') as f:
#         f.write(png_data)
    
# except Exception as e:
#     raise(e)

from reflex.agent.interfaces.agent import IAgent
from reflex.api.api import FastAPIendpoint
from reflex.agent.mock_agent import MockAgent
from chainlit.utils import mount_chainlit
  
agent = MockAgent()

fastapi_app = FastAPIendpoint(agent=agent).app

mount_chainlit(app=fastapi_app, target="./reflex/front/cl_entrypoint.py", path="/interface")

