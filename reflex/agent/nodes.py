from reflex.schema.states import MessageState
from loguru import logger
from reflex.agent.interfaces.node import INodes



class ReflexNodes(INodes):
    def __init__(self, generate_prompt: str, decide_prompt: str) -> None:
        self.generate_prompt = generate_prompt
        self.decide_prompt = decide_prompt
        super().__init__()

    @staticmethod
    def generate_query_or_respond(state: MessageState):
        """Decide whether to generate a query or respond directly."""
        # Create a messages list with the decide prompt as system message
        messages_with_prompt = [
            {"role": "system", "content": state["decide_prompt"]},
            *state["messages"]
        ]
        
        response = (
            state["chat_model"]
            .bind_tools([state["retrieve_tool"]])
            .invoke(messages_with_prompt)
        )
        logger.info(f"Decided to {'use tools' if response.additional_kwargs.get('tool_calls') else 'respond directly'}")
        return {"messages": [response]}

    @staticmethod
    def generate_answer(state: MessageState):
        """Generate an answer."""
        question = state["messages"][0].content
        context = state["messages"][-1].content
        prompt = state["generate_prompt"].format(question=question, context=context)
        response = state["chat_model"].invoke([{"role": "user", "content": prompt}])
        return {"messages": [response]}


