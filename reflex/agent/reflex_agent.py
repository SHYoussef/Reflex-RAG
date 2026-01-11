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
    def __init__(self, retriever: BaseRetriever, generate_prompt: str, decide_prompt:str, openai_api_key: str, temperature:int, model_name:str, State = MessageState)-> None:
        self.graph_builder = StateGraph(State)
        self.generate_prompt = generate_prompt
        self.decide_prompt = decide_prompt
        self.temperature = temperature
        self.openai_api_key = openai_api_key
        self.model_name = model_name
        self.chat_model = self._init_openai_chat_model()
        self.retriever = retriever
        self._add_nodes()
        self._add_edges()
        self.graph = self._build_graph()
        

    def _init_openai_chat_model(self) -> ChatOpenAI:
        return ChatOpenAI(model_name=self.model_name, temperature=self.temperature, openai_api_key=self.openai_api_key)
    
    def generate_answer(self, question: str) -> str:
        init_state = {
            "messages": [{"role": "user", "content": question}],
        }
        response = self.graph.invoke(init_state)
        return response["messages"][-1].content

    # Agent building methods
    def _add_nodes(self) -> None:
        self.graph_builder.add_node("generate_query_or_respond", self.generate_query_or_respond)
        self.graph_builder.add_node("respond", self.respond)
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
        self.graph_builder.add_edge("retrieve", "respond")
        self.graph_builder.add_edge("respond", END)
        logger.info("successfully added edges to the graph")

    def _build_graph(self)-> None:
        return self.graph_builder.compile()

    ## Nodes
    def generate_query_or_respond(self, state: MessageState):
        """Decide whether to generate a query or respond directly."""
        # Create a messages list with the decide prompt as system message
        messages_with_prompt = [
            {"role": "system", "content": self.decide_prompt},
            *state["messages"]
        ]
        
        response = (
            self.chat_model
            .bind_tools([self._create_tool_for_retrieve()])
            .invoke(messages_with_prompt)
        )
        logger.info(f"Decided to {'use tools' if response.additional_kwargs.get('tool_calls') else 'respond directly'}")
        return {"messages": [response]}

    def respond(self, state: MessageState):
        """Generate an answer."""
        question = state["messages"][0].content
        context = state["messages"][-1].content
        prompt = self.generate_prompt.format(question=question, context=context)
        response = self.chat_model.invoke([{"role": "user", "content": prompt}])
        return {"messages": [response]}

    ## Retriever Tool
    def _create_tool_for_retrieve(self)-> Tool:
        retriever_tool = create_retriever_tool(
            self.retriever,
            self.retriever.name,
            self.retriever.description,
        )
        return retriever_tool
    


    