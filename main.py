import openai
from dotenv import load_dotenv
import os
import time
import logging
from datetime import datetime


# Load environment variables from a .env file
load_dotenv()

# Retrieve the API key from the environment variable
API_KEY = "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"

# Ensure the API key is set
# if not API_KEY:
#     raise ValueError("API key not found. Please set the OPENAI_API_KEY environment variable.")

# # Set the API key for the OpenAI client
openai.api_key = API_KEY

# Initialize the OpenAI client
client = openai.OpenAI(api_key=API_KEY)
model = "gpt-3.5-turbo"

# # Creating our Assistant
# personal_assistant = client.beta.assistants.create(
#     name="Aurora - Personal Assistant",
#     instructions="""You are a personal assistant. You can help with a variety of tasks, such as scheduling, booking, and other tasks that a personal assistant might do. You can also answer questions and have conversations. You can provide information and send emails, and more. You can also provide recommendations for products, services, and other things. You can help with a variety of tasks, such as scheduling, booking, and other tasks that a personal assistant might do. You can also answer questions and have conversations. You can provide information, make calls, send emails, and more. You can also provide recommendations for products, services, and other things.""",
#     model=model
# )


# assistant_id = personal_assistant.id
# print(assistant_id)

# # Create a thread
# thread = client.beta.threads.create(
#     messages=[
#         {
#             "role": "user",
#             "content": "Hello what can you do for me?",
#         }
#     ]
# )
# thread_id = thread.id
# print(thread_id)

#Hardcoding ids
assistant_id = "asst_CAF20m8kJo87F6twxSKGxwj8"
thread_id = "thread_X90yeEVFQYUJKXYalHTYeoKb"

# Send a message to the assistant
message = "Can you "
message = client.beta.threads.messages.create(
    thread_id=thread_id,
    role = "user",
    content=message
)


# Get the response from the assistant
run = client.beta.threads.runs.create(
    thread_id=thread_id,
    assistant_id=assistant_id,
)

def get_response(client,thread,run_id,sleep_time=1):

    while True:
        try:
            run = client.beta.threads.run.retrieve(thread_id=thread_id, run_id=run_id)
            if run.completed_at:
                elapsed_time = run.completed_at - run.created_at
                print(f"Elapsed time: {elapsed_time}")
                messages = client.beta.threads.messages.list(thread_id=thread_id)
                last_message = messages.data[0]
                response = last_message.content[0].text.value
                print(f"Response: {response}")
                break
        except Exception as e:
            print(f"Error: {e}")
            break
        time.sleep(sleep_time)

get_response(client,thread_id,run_id=run.id)
