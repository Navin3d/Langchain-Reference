import asyncio

from langchain_ollama import ChatOllama
from langchain_core.runnables import RunnableSequence, RunnableParallel
from langchain.prompts import ChatMessagePromptTemplate
from langchain_core.tools import tool

from langchain_mcp_adapters.client import MultiServerMCPClient


llm = ChatOllama(model="qwen2.5:latest", temperature=0.7, streaming=False)

res = llm.invoke("hi")
print(res)


async def main():
    async with MultiServerMCPClient(
            {
                "MongoDB": {
                    "type": "stdio",
                      "command": "npx",
                      "args": [
                        "-y",
                        "mongodb-mcp-server@latest",
                        "--readOnly"
                      ],
                    "env": {"DEBUG": "mcp*"}
                }
            }
        ) as client:
            tools = client.get_tools()
            print(tools)

            # llm.bind_tools([tools])
            #
            # res = llm.ainvoke("total no of databases present")
            # print(res)



loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
try:
    loop.run_until_complete(main())
finally:
    loop.run_until_complete(loop.shutdown_asyncgens())
    loop.close()