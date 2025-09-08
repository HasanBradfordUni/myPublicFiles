import pandas as pd
from google.cloud import texttospeech as tts
import os

# Initialize the Text-to-Speech client
client = tts.TextToSpeechClient()

# Function to synthesize speech
def synthesize_speech(text, output_file):
    input_text = tts.SynthesisInput(text=text)
    voice = tts.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=tts.SsmlVoiceGender.NEUTRAL
    )
    audio_config = tts.AudioConfig(
        audio_encoding=tts.AudioEncoding.MP3
    )
    response = client.synthesize_speech(
        input=input_text,
        voice=voice,
        audio_config=audio_config
    )
    with open(output_file, "wb") as out:
        out.write(response.audio_content)

# Load the dataset
data = pd.read_csv('Conversation.csv')

# Create directories for questions and answers if they don't exist
os.makedirs('questions', exist_ok=True)
os.makedirs('answers', exist_ok=True)

# Ensure the columns are named 'Question' and 'Answer'
for index, row in data.iterrows():
    # Prepare the text
    question_text = f"Question: {row['question']}"
    answer_text = f"Answer: {row['answer']}"

    # Convert text to speech and save the audio files in their respective directories
    synthesize_speech(question_text, f"questions/question_{index}.mp3")
    synthesize_speech(answer_text, f"answers/answer_{index}.mp3")

    print(f"Saved questions/question_{index}.mp3 and answers/answer_{index}.mp3")

print("All audio files have been created successfully.")
