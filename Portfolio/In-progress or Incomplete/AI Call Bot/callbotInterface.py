import tkinter as tk
from tkinter import filedialog
from geminiPrompt import *
from time import sleep
from PIL import ImageTk, Image
from pydub import AudioSegment
from pydub.playback import play
from elevenLabs import generate_kingkong_voice
import os, threading
import uvicorn
from fastapi import FastAPI, Request

#Function to play the audio
def play_audio(audio_path):
    try:
        # Check if file exists
        if not os.path.exists(audio_path):
            print(f"Audio file not found: {audio_path}")
            return
            
        audio = AudioSegment.from_file(audio_path)
        play(audio)
    except FileNotFoundError:
        print("Error: FFmpeg not found. Please install FFmpeg and add it to your PATH.")
    except Exception as e:
        print(f"Error playing audio: {e}")

def start_conversation():
    try:
        # First ask for input file path
        input_audio_path = filedialog.asksaveasfilename(
            defaultextension=".wav", 
            filetypes=[("WAV files", "*.wav")]
        )
        
        if not input_audio_path:  # User cancelled
            return
            
        # Record audio
        duration = 10
        print("Recording...")
        record_audio(input_audio_path, duration)
        print("Recording finished.")
        sleep(1)
        
        # Ask for output file path
        output_audio_path = filedialog.asksaveasfilename(
            defaultextension=".wav", 
            filetypes=[("WAV files", "*.wav")]
        )
        
        if not output_audio_path:  # User cancelled
            return
            
        # Process message
        try:
            print("Processing message...")
            text = process_user_message(input_audio_path, output_audio_path)
            generate_kingkong_voice(text)
            print("Processing complete.")
        except Exception as e:
            print(f"Error processing message: {e}")
        
        # Play audio if file exists
        if os.path.exists(output_audio_path):
            print("Playing response...")
            play_audio(output_audio_path)
        else:
            print(f"Output audio file not found: {output_audio_path}")
            
    except Exception as e:
        print(f"Error in conversation flow: {e}")

root = tk.Tk()
root.title("AI Call Bot")
root.geometry("300x500")

header_label = tk.Label(root, text="King Kong AI Call Bot", font=("Arial", 22))
header_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

# Get directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(script_dir, "images", "KingKong.png")
image1 = Image.open(image_path)
img=image1.resize((138, 110))

my_img=ImageTk.PhotoImage(img)

my_label = tk.Label(root, image=my_img)
my_label.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

mic_button = tk.Button(root, text="🎤", command=start_conversation, font=("Arial", 22))
mic_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# Initialize FastAPI app
app = FastAPI()

# At the end of your file, before root.mainloop()
def run_webhook():
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Start webhook in a separate thread
webhook_thread = threading.Thread(target=run_webhook, daemon=True)
webhook_thread.start()

# Run the application
root.mainloop()
