import requests
from pydub import AudioSegment
from pydub.effects import speedup
from pydub.playback import play
import os
import subprocess

# ===== FFMPEG CONFIGURATION =====
ffmpeg_dir = r"C:\Users\fifau\AppData\Local\Programs\Python\Python312\Scripts\ffmpeg-2025-06-23-git-e6298e0759-essentials_build\bin"
AudioSegment.ffmpeg = os.path.join(ffmpeg_dir, "ffmpeg.exe")
AudioSegment.ffprobe = os.path.join(ffmpeg_dir, "ffprobe.exe")

if not all(os.path.exists(p) for p in [AudioSegment.ffmpeg, AudioSegment.ffprobe]):
    raise RuntimeError("FFmpeg not found. Please install or update path.")

# ===== ELEVENLABS CONFIG =====
API_KEY = "sk_42bf9d447322336059fcee1a61ad1d2eeb3a7c02f06330c6"  # Private API Key from Eleven Labs
VOICE_ID = "ehrmToLOHnIm9KrbrPBa"  # Custom Voice ID for King Kong
TEMP_FILE = "temp_kingkong.wav"  # Changed to WAV
FINAL_FILE = "kingkong_final.wav"  # Changed to WAV

def generate_kingkong_voice(text):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {
        "xi-api-key": API_KEY,
        "Content-Type": "application/json",
        "Accept": "audio/wav"
    }
    data = {
        "text": text,
        "voice_settings": {
            "stability": 0.3,
            "similarity_boost": 0.8,
            "style": 0.5,
            "speaker_boost": True
        }
    }
    
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 200:
        with open(TEMP_FILE, "wb") as f:
            f.write(response.content)
        return True
    else:
        print("API Error:", response.text)
        return False

def deepen_voice(input_file, output_file):
    try:
        audio = AudioSegment.from_wav(input_file)
        slowed = speedup(audio, playback_speed=0.85)
        pitched = slowed._spawn(
            slowed.raw_data,
            overrides={"frame_rate": int(slowed.frame_rate * 0.7)}
        )
        pitched = pitched + 5
        pitched.export(output_file, format="wav")
        return True
    except Exception as e:
        print(f"Audio processing error: {str(e)}")
        return False

def kingkong_speak(text):
    if not generate_kingkong_voice(text):
        return None
    
    if deepen_voice(TEMP_FILE, FINAL_FILE):
        # Return the audio data for sending via WhatsApp
        with open(FINAL_FILE, 'rb') as f:
            audio_data = f.read()
        
        if os.path.exists(TEMP_FILE):
            os.remove(TEMP_FILE)
        if os.path.exists(FINAL_FILE):
            os.remove(FINAL_FILE)
            
        return audio_data
    return None

if __name__ == "__main__":
    try:
        while True:
            text = input("\nEnter text for King Kong (or 'quit' to exit): ")
            if text.lower() == 'quit':
                break
            kingkong_speak(text)
    except:
        print("An error occurred. Exiting...")