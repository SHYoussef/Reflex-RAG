from reflex.agent.reflex_agent import ReflexAgent
from reflex.agent.tools import PineconeRetriever
from reflex.utils.config import get_agent_config

import chainlit as cl
  


config = get_agent_config()

retriever_cl = PineconeRetriever(
    top_k=config.retriever.top_k,
    pinecone_api_key=config.retriever.pinecone_api_key,
    index_name=config.retriever.index_name,
    rerank_model=config.retriever.rerank_model,
    top_n=config.retriever.top_n)
agent_cl = ReflexAgent(retriever = retriever_cl, generate_prompt=config.generate.generate_prompt, decide_prompt=config.generate.decide_prompt, openai_api_key=config.generate.openai_api_key, temperature=config.generate.temperature, model_name=config.generate.model_name)
 

@cl.on_chat_start
async def on_chat_start():
    await cl.Message(config.chainlit.welcome_message).send()

@cl.on_message
async def on_message(message: cl.Message):
    question = message.content
    answer = agent_cl.generate_answer(question)
    await cl.Message(answer).send()

