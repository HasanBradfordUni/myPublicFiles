#Importing the modules
import vertexai
from vertexai.generative_models import GenerativeModel
import google.auth

from aiCallChatbot import *
from testConversation import *

credentials, project_id = google.auth.default()

vertexai.init(project="generalpurposeai", location="us-central1")

model = GenerativeModel(model_name="gemini-1.5-pro")

input_audio_path = input("Enter the path to save the audio: ")
record_audio(input_audio_path, duration=5)

# Transcribe the question
transcribed_question = transcribe_audio(input_audio_path)
print(f"User: {transcribed_question}")

prompt = f"You are a chatbot character with the personality of King Kong the goriila. You are having a conversation with a human. The human says: {transcribed_question}"
if prompt != "":
    responses = model.generate_content(prompt, stream=True)
    for response in responses:
        print(response.text)
else:
    exit()
