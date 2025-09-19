from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
import os
from dotenv import load_dotenv
import datetime
import json

load_dotenv()

app = FastAPI()

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "king_kong_verify123")  # Replace with your actual token

# ✅ Verification route (GET)
@app.get("/")
async def verify_webhook(request: Request):
    params = dict(request.query_params)
    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("WEBHOOK VERIFIED")
        return PlainTextResponse(challenge)
    else:
        return PlainTextResponse("Forbidden", status_code=403)

# ✅ Event handler route (POST)
@app.post("/")
async def receive_webhook(request: Request):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = await request.json()
    print(f"\n\nWebhook received {timestamp}\n")
    print(json.dumps(data, indent=2))
    return {"status": "received"}
