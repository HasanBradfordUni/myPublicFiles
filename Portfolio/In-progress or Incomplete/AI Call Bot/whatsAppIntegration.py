from elevenLabs import kingkong_speak, generate_kingkong_voice, deepen_voice
import requests, os, json
from pydub import AudioSegment
# Add to your existing imports
from fastapi import FastAPI, Request
import uvicorn

# Constants for Evolution API
EVOLUTION_API_URL="https://your-evolution-api-server.com"
EVOLUTION_API_KEY="your-api-key-here"
EVOLUTION_API_INSTANCE="your-instance-name"

# Initialize FastAPI app
app = FastAPI()

# Webhook endpoint for call events
@app.post("/whatsapp-webhook")
async def whatsapp_webhook(request: Request):
    data = await request.json()
    
    # Check if it's a call event
    if data.get("event") == "call":
        call_id = data.get("call_id")  # e.g. "omnZfTjnOQxFEFEfs0R4ql"
        from_number = data.get("from")
        
        # Process the call (your existing logic)
        response_text = "ROAR! This is King Kong speaking!"
        generate_kingkong_voice(response_text)
        
        # Join the call and play audio
        join_whatsapp_call(call_id, "kingkong_final.wav")
        
        return {"status": "success"}
    
    return {"status": "ignored"}

def join_whatsapp_call(call_id, audio_file):
    """Function to join WhatsApp call using Evolution API"""
    url = f"{EVOLUTION_API_URL}/call/join"
    headers = {
        "apikey": EVOLUTION_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "call_id": call_id,
        "audio_file": audio_file
    }
    
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
    call_id = input("Enter call ID to join: ")
    audio_file = input("Enter audio file path to play: ")
    join_whatsapp_call(call_id, audio_file)