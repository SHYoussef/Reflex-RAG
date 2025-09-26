from langgraph.graph import StateGraph, START, END
from reflex.agent.interfaces.agent import IAgent
from reflex.agent.interfaces.node import INodes
from reflex.agent.nodes import ReflexNodes

from reflex.schema.states import MessageState, ClassifierState
from typing import Literal

from logging import Logger



class ReflexAgent(IAgent):
    def __init__(self, nodes:INodes, State = MessageState):
        self.graph_builder = StateGraph(State)
        self.nodes = nodes
        self._add_nodes(self.nodes)
        self._add_edges()
        self.graph = self._build_graph()
        
    def generate_answer(self) -> None:
        return None

    def _add_nodes(self, nodes: INodes) -> None:

        for func_name in nodes.all_methods:
            # bind the function to the instance of `nodes`
            bound_func = getattr(nodes, func_name)
            self.graph_builder.add_node(func_name, bound_func)


    def _build_graph(self)-> None:
        return self.graph_builder.compile()
    
    @staticmethod
    def classification_router(state: ClassifierState) -> Literal["answer_with_sources", "answer_without_sources"]:
        if state["classification"] == "retrieve":
            return "answer_with_sources"
        elif state["classification"] =="answer":
            return "answer_without_sources"
        else:
            Logger.warning("incorrect classification has been made")
            raise(ValueError("INCORRECT CLASSIFICATION"))

    def _add_edges(self) -> None:
        self.graph_builder.add_edge(START, "classifier_node")
        self.graph_builder.add_conditional_edges("classifier_node", self.classification_router)
        self.graph_builder.add_edge("answer_without_sources", END)
        self.graph_builder.add_edge("answer_with_sources", END)

