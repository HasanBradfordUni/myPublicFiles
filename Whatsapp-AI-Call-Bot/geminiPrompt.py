#Importing the modules
import vertexai
from vertexai.generative_models import GenerativeModel
import google.auth

from aiCallChatbot import *
from testConversation import *
import pyperclip

credentials, project_id = google.auth.default()

vertexai.init(project="generalpurposeai", location="us-central1")

model = GenerativeModel(model_name="gemini-2.0-flash")

def process_user_message(input_audio_path, output_audio_path):
    try:
        # Transcribe the question
        transcribed_question = transcribe_audio(input_audio_path)
        print(f"User: {transcribed_question}")
        prompt = f"You are a chatbot character with the personality of King Kong the goriila. You are having a conversation with a human. The human says: {transcribed_question}"
        text = ""
        if prompt != "":
            responses = model.generate_content(prompt, stream=True)
            print("King Kong: ")
            for response in responses:
                text += response.text
                print(response.text)
        synthesize_speech(text, output_audio_path)
    except google.api_core.exceptions.ServiceUnavailable as e:
        print(f"Google API service unavailable: {e}")
        # Create a simple fallback response
        fallback_text = "I'm sorry, the service is currently unavailable. Please try again later."
        synthesize_speech(text, output_audio_path)
    except Exception as e:
        print(f"An error occurred: {e}")
        fallback_text = "I'm sorry, there was an error processing your request."
        synthesize_speech(text, output_audio_path)
    return text

if __name__ == "__main__":
    #input_audio_path = input("Enter the path to save the audio: ")
    #record_audio(input_audio_path, duration=5)

    # Transcribe the question
    #transcribed_question = transcribe_audio(input_audio_path)
    transcribed_question = input("Enter your question for King Kong: ")
    print(f"User: {transcribed_question}")

    prompt = f"You are a chatbot character with the personality of King Kong the goriila. You are having a conversation with a human. The human says: {transcribed_question}"
    total_text = ""
    if prompt != "":
        responses = model.generate_content(prompt, stream=True)
        print(responses)
        for response in responses:
            print(response.text)
            total_text += response.text
        pyperclip.copy(total_text)
        print("Response copied to clipboard.")
    else:
        exit()
