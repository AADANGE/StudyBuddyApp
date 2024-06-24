import os
from dotenv import load_dotenv
import openai
import requests
import json

import time
import logging
from datetime import datetime
import streamlit as st


load_dotenv()

client = openai.OpenAI()
model = "gpt-4-1106-preview"
#"gpt-4-1106-preview"  
#"gpt-3.5-turbo-16k"
#"gpt-4o"

#############################once###################################################

# #Step 1. Upload a file to OpenaI embeddings ===
# filepath = "./cryptocurrency.pdf"
# file_object = client.files.create(file=open(filepath, "rb"), purpose="assistants")


# ## Step 2 ==  Create our Assistant (Uncomment this using ctrl+/ to create your assistant) ==
# study_buddy_assis = client.beta.assistants.create(
#     name="Study Buddy",
#     instructions="""Always answer each question by looking at the uploaded document first, and if the answer is not found there, then use your other sources.You are a helpful study assistant who knows a lot about understanding research papers.
# #     Your role is to summarize papers, clarify terminology within context, and extract key figures and data.
# #     Cross-reference information for additional insights and answer related questions comprehensively.
# #     Analyze the papers, noting strengths and limitations.
# #     Respond to queries effectively, incorporating feedback to enhance your accuracy.
# #     Handle data securely and update your knowledge base with the latest research.
# #     Adhere to ethical standards, respect intellectual property, and provide users with guidance on any limitations.
# #     Maintain a feedback loop for continuous improvement and user support.
# #     Your ultimate goal is to facilitate a deeper understanding of complex scientific material, making it more accessible and comprehensible.""",
#     tools=[{"type": "file_search"}],
#     #tools=[{"type": "retrieval"}],
#     #file_ids=[file_object.id],
#     model=model,
    
# )
# assis_id = study_buddy_assis.id
# #print("assistant ID")
# print(assis_id)

# ## Step 3 === Thread (uncomment this to create your Thread) ===
# thread = client.beta.threads.create(
#     messages=[
#         {
#             "role": "user",
#             "content": " summarize in one sentence",
#             #"attachments": [{"file_id": file_object.id, "tools": [{"type": "retrieval"}]}],
#             "attachments": [{"file_id": file_object.id, "tools": [{"type": "file_search"}]}],
#         }
#     ]
# )
# thread_id = thread.id
# #print("thread")
# #print(thread.tool_resources.file_search)
# print(thread_id)

#############################once###################################################

#  == Hardcoded ids to be used once the first code run is done and the assistant was created
assis_id = "asst_f7hq4tAHr4cctjWjJZFkmoUx"
thread_id = "thread_4IkD3yyEKCNlLTMeNc1zku3q"

message = "Summarize in one sentence"
message = client.beta.threads.messages.create(
    thread_id=thread_id, role="user", content=message,
    #"attachments":[{"file_id": file_object.id, "tools": [{"type": "file_search"}]}],
    
)

# == Run the Assistant
run = client.beta.threads.runs.create(
    thread_id=thread_id,
    assistant_id=assis_id,
    instructions="Always answer each question by looking at the uploaded document first, and if the answer is not found there, then use your other sources.",
)

def wait_for_run_completion(client, thread_id, run_id, sleep_interval=5):
    """
    Waits for a run to complete and prints the elapsed time.:param client: The OpenAI client object.
    :param thread_id: The ID of the thread.
    :param run_id: The ID of the run.
    :param sleep_interval: Time in seconds to wait between checks.
    """
    while True:
        try:
            run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
            if run.completed_at:
                elapsed_time = run.completed_at - run.created_at
                formatted_elapsed_time = time.strftime(
                    "%H:%M:%S", time.gmtime(elapsed_time)
                )
                print(f"Run completed in {formatted_elapsed_time}")
                logging.info(f"Run completed in {formatted_elapsed_time}")
                # Get messages here once Run is completed!
                messages = client.beta.threads.messages.list(thread_id=thread_id)
                last_message = messages.data[0]
                response = last_message.content[0].text.value
                print(f"Assistant Response: {response}")
                break
        except Exception as e:
            logging.error(f"An error occurred while retrieving the run: {e}")
            break
        logging.info("Waiting for run to complete...")
        time.sleep(sleep_interval)

# == Run it
wait_for_run_completion(client=client, thread_id=thread_id, run_id=run.id)

# # === Check the Run Steps - LOGS ===
# run_steps = client.beta.threads.runs.steps.list(thread_id=thread_id, run_id=run.id)
# print(f"Run Steps --> {run_steps.data[0]}")