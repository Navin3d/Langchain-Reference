from typing import TypedDict, Annotated

from dotenv import load_dotenv
load_dotenv()

from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.constants import END
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages

from chains import generation_chain, reflection_chain


class MessageGraph(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

GENERATE_NODE = 'generate'
REFLECT_NODE = 'reflect'

def generation_node(state: MessageGraph):
    return {
        "messages": generation_chain.invoke(
            {
                "messages": state["messages"]
            }
        )
    }

def reflection_node(state: MessageGraph):
    reflection_response = reflection_chain.invoke(
        {
            "messages": state["messages"]
        }
    )
    return {
        "messages": HumanMessage(content=reflection_response.content)
    }

graph_builder = StateGraph(state_schema=MessageGraph)
graph_builder.add_node(GENERATE_NODE, generation_node)
graph_builder.add_node(REFLECT_NODE, reflection_node)
graph_builder.set_entry_point(GENERATE_NODE)

def should_continue(state: MessageGraph):
    if len(state["messages"]) > 6:
        return END
    return REFLECT_NODE

graph_builder.add_conditional_edges(GENERATE_NODE, should_continue, path_map={END:END, REFLECT_NODE:REFLECT_NODE})
graph_builder.add_edge(REFLECT_NODE, GENERATE_NODE)

graph = graph_builder.compile()
print(graph.get_graph().draw_mermaid())

if __name__ == '__main__':
    print("Reflection Agent")
    inputs = {
        "messages": [
            HumanMessage(
                content="""Make this tweet better:"
                                        @LangChainAI
                — newly Tool Calling feature is seriously underrated.

                After a long wait, it's  here- making the implementation of agents across different models with function calling - super easy.

                Made a video covering their newest blog post

                                      """
            )
        ]
    }
    response = graph.invoke(inputs)
    print(response)
