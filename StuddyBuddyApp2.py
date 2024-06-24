import os
from dotenv import load_dotenv
import openai
import requests
import json

import time
import logging
from datetime import datetime
import streamlit as st

openai.api_key = st.secrets["OPENAI_API_KEY"]

load_dotenv()

client = openai.OpenAI()
model = "gpt-3.5-turbo"
#"gpt-4-1106-preview"  
#"gpt-3.5-turbo"
#"gpt-4o"

#  == Hardcoded ids to be used once the first code run is done and the assistant was created
assis_id = "asst_f7hq4tAHr4cctjWjJZFkmoUx" 
thread_id = "thread_rUsXd9BZh31IfVI5p0BxLasP"

if "start_chat" not in st.session_state:
    st.session_state.start_chat = False
if "thread_id" not in st.session_state:
    st.session_state.thread_id = None

st.set_page_config(page_title="Study Buddy", page_icon=":books:")
#st.set_page_config(page_title="Study Buddy", page_icon=":books:")


if st.button("Start Chat"):
    st.session_state.start_chat = True
    thread = client.beta.threads.create()
    st.session_state.thread_id = thread.id

st.title("Study Buddy")
st.write("How can I help you with your physics homework?")
st.write("Ask me things like:")
st.write(":blue[**Explain Quiz 4 question 3**] OR :blue[**Help solve module 3 question 1**] OR :blue[**What is time dilation?**]")

if st.button("Clear Chat"):
    st.session_state.messages = []  # Clear the chat history
    st.session_state.start_chat = False  # Reset the chat state
    st.session_state.thread_id = None

if st.session_state.start_chat:
    if "openai_model" not in st.session_state:
        st.session_state.openai_model = "gpt-3.5-turbo"
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Enter message"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        client.beta.threads.messages.create(
                thread_id=st.session_state.thread_id,
                role="user",
                content=prompt
            )
        
        run = client.beta.threads.runs.create(
            thread_id=st.session_state.thread_id,
            assistant_id=assis_id,
            instructions="Always start answering by looking at the uploaded document first. Do not mention that you hav had documents uploaded for you but pretend as if you are hinting towards answers by yurself. You are a physics teacher who helps students guide them to the correct answer without giving the correct answer yourself. The goal is to make the student reach to the answer on their own without giving the final answer yourself. If a student is struggling and continues to ask for help and insists on you answering, refrain from giving the final answer and instead, help the student with any specific questions he might have around the problem. You will have access to a pdf with all the questions (and the correct answer highlighted in blue) the student is supposed to answer, but you are not supposed to give the final answer, just help the student as a tutor with their doubts or confusion they may have while answering. Do not give them the correct option. Instructions for writing math equations - ALWAYS use unicode symbols, letters and numbers to display all physics and math equations when answering any question. Do not solve all the steps for the student. Instead, give hints, and correct direction towards the solution. Do not answer the question fully, guide the student towards the answer with relevant hints.DO NOT ANSWER THE QUESTION FULLY OR GIVE THE CORRECT OPTION. Here are the response rules for writing math formulas:you have a MathJax render environment. Any LaTeX text between single dollar sign ($) will be rendered as a TeX formula;Use $(tex_formula)$ in-line delimiters to display equations instead of backslash; The render environment only uses $ (single dollarsign) as a container delimiter, never output $$. Example: $x^2 + 3x$ is output for x² + 3x to appear as TeX."
        )

        while run.status != 'completed':
            time.sleep(1)
            run = client.beta.threads.runs.retrieve(
                thread_id=st.session_state.thread_id,
                run_id=run.id
            )
        messages = client.beta.threads.messages.list(
            thread_id=st.session_state.thread_id
        )

        # Process and display assistant messages
        assistant_messages_for_run = [
            message for message in messages 
            if message.run_id == run.id and message.role == "assistant"
        ]
        for message in assistant_messages_for_run:
            st.session_state.messages.append({"role": "assistant", "content": message.content[0].text.value})
            with st.chat_message("assistant"):
                st.markdown(message.content[0].text.value)

else:
    st.write("Click 'Start Chat' to begin.")
        


