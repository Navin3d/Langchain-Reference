from datetime import datetime

from langchain_core.output_parsers import JsonOutputToolsParser, PydanticToolsParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableSequence
from langchain_ollama import ChatOllama

from schemas import AnswerQuestion

llm = ChatOllama(
    model=os.environ['MODEL_NAME'],
    temperature=0.7
)
parser = JsonOutputToolsParser(return_id=True)
parser_pydantic = PydanticToolsParser(tools=[AnswerQuestion])

actor_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are expert researcher.
        Current time: {time}

        1. {first_instruction}
        2. Reflect and critique your answer. Be severe to maximize improvement.
        3. Recommend search queries to research information and improve your answer.""",
    ),
    MessagesPlaceholder(variable_name="messages"),
    ("system", "Answer the user's question above using the required format."),
]).partial(
    time=lambda: datetime.now().isoformat(),
)

first_response_prompt = actor_prompt.partial(
    first_instruction="Provide a detailed ~250 word answer"
)

first_responder = RunnableSequence(first_response_prompt, llm.bind_tools(
    tools=[AnswerQuestion], tool_choice="AnswerQuestion"
))

revise_instructions = """Revise your previous answer using the new information.
    - You should use the previous critique to add important information to your answer.
        - You MUST include numerical citations in your revised answer to ensure it can be verified.
        - Add a "References" section to the bottom of your answer (which does not count towards the word limit). In form of:
            - [1] https://example.com
            - [2] https://example.com
    - You should use the previous critique to remove superfluous information from your answer and make SURE it is not more than 250 words.
"""
