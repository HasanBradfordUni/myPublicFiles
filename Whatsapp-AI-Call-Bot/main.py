from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
import os, datetime, json
from dotenv import load_dotenv
from geminiPrompt import process_user_message
import requests

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

    send_whatsapp_message(sender, response_text)

def send_whatsapp_message(recipient_number, message_text):
    phone_number_id = os.getenv("699760716561335")
    access_token = os.getenv("EAAYZChY2VuvoBPJU2SuaTmVf9wyCn4G7n9MDDfop2jHvkg4xjZBlEdVZCZCESEjwVSF261tKusiUoE7kvMOgNPbgF4ELk0FTyHkofHVsbYctDrW4cpoZB0vxxCs1khX8sHxCIfq0G4WYcjvjX93IYkRlZAkMz4j8cO7gFaPDBuhz7yaMzofJNxx3ZB11C4fyZAHgAmdZBaBujZAciP")

    url = f"https://graph.facebook.com/v19.0/{phone_number_id}/messages"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": recipient_number,
        "type": "text",
        "text": {
            "body": message_text
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    print("WhatsApp API response:", response.status_code, response.text)


