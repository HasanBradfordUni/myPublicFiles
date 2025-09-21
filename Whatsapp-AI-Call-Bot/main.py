from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
import os, datetime, json
from dotenv import load_dotenv
from geminiPrompt import process_user_message

load_dotenv()
app = FastAPI()

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "king_kong_verify123")

@app.get("/")
async def verify_webhook(request: Request):
    params = dict(request.query_params)
    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("WEBHOOK VERIFIED")
        return PlainTextResponse(challenge)
    return PlainTextResponse("Forbidden", status_code=403)

@app.post("/")
async def receive_webhook(request: Request):
    data = await request.json()
    print(f"\nWebhook received {datetime.datetime.now()}\n{json.dumps(data, indent=2)}")

    message = data.get("entry", [{}])[0].get("changes", [{}])[0].get("value", {}).get("messages", [{}])[0]
    sender = message.get("from")
    text = message.get("text", {}).get("body", "")

    if "callID:" in text or "join:" in text:
        call_id = extract_call_id(text)
        handle_call_request(call_id, sender)
    else:
        respond_as_king_kong(text, sender)

    return {"status": "processed"}

def extract_call_id(text):
    if "callID:" in text:
        return text.split("callID:")[1].strip()
    elif "join:" in text:
        return text.split("join:")[1].strip()
    return None

def handle_call_request(call_id, sender):
    print(f"Received call request from {sender} to join call: {call_id}")
    # You can log, store, or trigger a future action here

def respond_as_king_kong(text, sender):
    input_audio_path = f"{sender}_input.wav"
    output_audio_path = f"{sender}_response.mp3"

    with open(input_audio_path, "wb") as f:
        f.write(text.encode())

    response_text = process_user_message(input_audio_path, output_audio_path)
    print(f"King Kong says: {response_text}")
    # You can send this response back via WhatsApp or store it for playback
