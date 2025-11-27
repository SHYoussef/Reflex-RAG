from langgraph.graph import StateGraph, START, END
from langchain.tools.retriever import create_retriever_tool
from langchain_core.retrievers import BaseRetriever
from langchain_core.tools.simple import Tool
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition
from langchain_openai import ChatOpenAI

from reflex.agent.interfaces.agent import IAgent
from reflex.agent.interfaces.node import INodes
from reflex.agent.nodes import ReflexNodes
from reflex.schema.states import MessageState


from loguru import logger


class ReflexAgent(IAgent):
    def __init__(self, nodes: ReflexNodes, retriever: BaseRetriever, openai_api_key: str, temperature:int, model_name:str, State = MessageState)-> None:
        self.graph_builder = StateGraph(State)
        self.nodes = nodes
        self.temperature = temperature
        self.openai_api_key = openai_api_key
        self.model_name = model_name
        self.chat_model = self._init_openai_chat_model()
        self.retriever = retriever
        self._add_nodes(self.nodes)
        self._add_edges()
        self.graph = self._build_graph()
        

    def _init_openai_chat_model(self) -> ChatOpenAI:
        return ChatOpenAI(model_name=self.model_name, temperature=self.temperature, openai_api_key=self.openai_api_key)
    
    def generate_answer(self, question: str) -> str:
        init_state = {
            "messages": [{"role": "user", "content": question}],
            "chat_model": self.chat_model,
            "retrieve_tool": self._create_tool_for_retrieve(),
            "generate_prompt": self.nodes.generate_prompt,
            "decide_prompt": self.nodes.decide_prompt,
        }
        response = self.graph.invoke(init_state)
        return response["messages"][-1].content

    def _add_nodes(self, nodes: INodes) -> None:

        for func_name in nodes.all_methods:
            bound_func = getattr(nodes, func_name)
            self.graph_builder.add_node(func_name, bound_func)
        # tool node for retrieval
        self.graph_builder.add_node("retrieve", ToolNode([self._create_tool_for_retrieve()]))
        logger.info("successfully added nodes to the graph")

    def _add_edges(self) -> None:
        self.graph_builder.add_edge(START, "generate_query_or_respond")

        self.graph_builder.add_conditional_edges(
            "generate_query_or_respond",
            tools_condition,
            {
                "tools": "retrieve",
                END: END,
            },
        )
        self.graph_builder.add_edge("retrieve", "generate_answer")
        self.graph_builder.add_edge("generate_answer", END)
        logger.info("successfully added edges to the graph")

    def _build_graph(self)-> None:
        return self.graph_builder.compile()
    
    def _create_tool_for_retrieve(self)-> Tool:
        retriever_tool = create_retriever_tool(
            self.retriever,
            self.retriever.name,
            self.retriever.description,
        )
        return retriever_tool
