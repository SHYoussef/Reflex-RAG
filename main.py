from IPython.display import Image, display
from reflex.graph.graph import ReflexAgent
from reflex.graph.nodes import ReflexNodes

nodes = ReflexNodes()
reflex_agent = ReflexAgent(nodes=nodes)


try:
    # Get the PNG data
    png_data = reflex_agent.graph.get_graph().draw_mermaid_png()
    
    # Save to file
    with open('./reflex_graph.png', 'wb') as f:
        f.write(png_data)
    
except Exception as e:
    raise(e)