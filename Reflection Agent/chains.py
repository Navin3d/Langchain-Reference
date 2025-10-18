import os

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableSequence
from langchain_ollama import ChatOllama


reflection_prompt = ChatPromptTemplate.from_messages([
    (
            "system",
            "You are a viral twitter influencer grading a tweet. Generate critique and recommendations for the user's tweet."
            "Always provide detailed recommendations, including requests for length, virality, style, etc."
    ),
    MessagesPlaceholder(variable_name="messages")
])

generation_prompt = ChatPromptTemplate.from_messages([
    (
            "system",
            "You are a twitter techie influencer assistant tasked with writing excellent twitter posts."
            " Generate the best twitter post possible for the user's request."
            " If the user provides critique, respond with a revised version of your previous attempts.",
    ),
    MessagesPlaceholder(variable_name="messages")
])

model_name = os.environ['MODEL_NAME']
llm = ChatOllama(
    model=model_name,
    temperature=0.7
)

reflection_chain = RunnableSequence(reflection_prompt, llm)
generation_chain = RunnableSequence(generation_prompt, llm)
