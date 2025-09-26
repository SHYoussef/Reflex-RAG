from reflex.schema.states import MessageState, ClassifierState
from typing import Literal
from logging import Logger
from reflex.agent.interfaces.node import INodes


class ReflexNodes(INodes):

    @staticmethod
    def classifier_node(messages: MessageState) -> ClassifierState:
        
        result = "answer"
        return {"messages": messages["messages"], "classification": result}

    @staticmethod
    def answer_without_sources(state: ClassifierState) -> MessageState:
        return {"messages": "Hello my G"}

    @staticmethod
    def answer_with_sources(state: ClassifierState) -> MessageState:
        return {"messages": "Hello my B"}
