from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
import os
import json
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Set up logging
logging.basicConfig(level=logging.INFO)

# ✅ Webhook verification route (Meta sends a GET request here)
@app.get("/whatsapp-webhook")
async def verify_webhook(request: Request):
    params = dict(request.query_params)
    verify_token = "kingkong_verify_123" # Actual verify token set in Meta App Dashboard    

    if params.get("hub.verify_token") == verify_token:
        challenge = params.get("hub.challenge")
        logging.info(f"Webhook verified with challenge: {challenge}")
        return PlainTextResponse(challenge)
    
    logging.warning("Webhook verification failed.")
    return PlainTextResponse("Verification failed", status_code=403)

# ✅ Webhook event handler (Meta sends POST requests here)
@app.post("/whatsapp-webhook")
async def handle_webhook(request: Request):
    try:
        data = await request.json()
        logging.info(f"Received WhatsApp webhook event:\n{json.dumps(data, indent=2)}")

        # You can add custom logic here to respond to messages, log statuses, etc.
        return {"status": "received"}
    
    except Exception as e:
        logging.error(f"Error processing webhook event: {e}")
        return {"status": "error", "message": str(e)}
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
