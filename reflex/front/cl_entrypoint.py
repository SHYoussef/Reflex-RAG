import chainlit as cl
from reflex.agent.interfaces.agent import IAgent

# Instantiate your agent (provide a real StateGraph if needed)
class MyAgent(IAgent):

    def generate_answer(self, question: str) -> str:
        return f"Agent's answer to: {question}"
    

agent = MyAgent()
@cl.on_chat_start
async def on_chat_start():
    await cl.Message("👋 Welcome to reflex rag, you could ").send()

@cl.on_message
async def on_message(message: cl.Message):
    question = message.content
    answer = agent.generate_answer(question)
    await cl.Message(answer).send()