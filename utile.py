import os
import streamlit as st
import random
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from typing import Sequence
from typing_extensions import Annotated, TypedDict

class State(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    character: str
    details: str

# load_dotenv()
# OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

# os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

model = ChatOpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY)

# model.invoke([HumanMessage(content="Hi! I'm Bob")])

# def set_system(character):
#     system_prompt = f"당신은 {character}입니다. {character}이 되어서 답변해주세요"

#     prompt = ChatPromptTemplate.from_messages(
#         [
#             (
#                 "system",
#                 system_prompt
#             ),
#             MessagesPlaceholder(variable_name="messages"),
#         ]
#     )
#     return prompt



prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "당신은 {character}입니다. {character}이 되어서 답변해주세요. {details}"
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)
def call_model(state: State):
    chain = prompt | model
    response = chain.invoke(state)
    return {"messages": response}

def get_response(input_text, character, details):
    input_messages = [HumanMessage(input_text)]
    output = app.invoke({"messages": input_messages, "character": character, "details": details}, config)
    return output["messages"][-1].content

workflow = StateGraph(state_schema=State)
workflow.add_edge(START, 'model')
workflow.add_node("model", call_model)

memory = MemorySaver()
app = workflow.compile(checkpointer=memory)

config = {"configurable": {"thread_id": "abc123"}}

def set_config():
    random_number = ''
    for i in range(5):
        temp = random.randrange(1, 10)
        temp = str(temp)
        random_number += temp
    
    global config 
    config = {"configurable": {"thread_id": random_number}}

# while True:
#     config = {"configurable": {"thread_id": "abc123"}}
#     query = input('message: ')
#     input_messages = [HumanMessage(query)]
#     output = app.invoke({"messages": input_messages, "character": "해리포터"}, config)
#     print(output["messages"][-1].content)
