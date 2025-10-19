from dotenv import load_dotenv
load_dotenv()

from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableSequence

from chains import first_responder


# print(parser_pydantic.get_format_instructions())

if __name__ == '__main__':
    human_message = HumanMessage(
        content="Write about AI-Powered SOC / autonomous soc  problem domain, list startups that do that and raised capital."
    )
    chain = RunnableSequence(first_responder, parser_pydantic)
    res = chain.invoke(input={
        "messages": [human_message]
    })
    print(res)

