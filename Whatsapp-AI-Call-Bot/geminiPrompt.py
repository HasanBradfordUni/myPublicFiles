import os
from google.generativeai import GenerativeModel
from pydub import AudioSegment
from openai import OpenAI
from elevenlabs import generate, save

def transcribe_audio(audio_path):
    audio = AudioSegment.from_file(audio_path)
    audio.export("temp.wav", format="wav")
    client = OpenAI()
    transcript = client.audio.transcriptions.create(model="whisper-1", file=open("temp.wav", "rb"))
    return transcript.text

def generate_king_kong_response(text):
    model = GenerativeModel("gemini-pro")
    prompt = f"You are King Kong. Respond to this message in your own voice and style:\n{text}"
    response = model.generate_content(prompt)
    return response.text

def synthesize_voice(text, output_path):
    audio = generate(text=text, voice="King Kong", model="eleven_multilingual_v2")
    save(audio, output_path)

def process_user_message(input_audio_path, output_audio_path):
    transcript = transcribe_audio(input_audio_path)
    kong_response = generate_king_kong_response(transcript)
    synthesize_voice(kong_response, output_audio_path)
    return kong_response
