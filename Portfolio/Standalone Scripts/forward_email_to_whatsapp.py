import imaplib
import email
import re
import pywhatkit as kit  # For sending WhatsApp messages
import time

# Step 1: Fetch the latest email
EMAIL_USER = "akhtarhasan2005@gmail.com"
EMAIL_PASSWORD = "ougg alha zarc rnmc"

def fetch_email():
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(EMAIL_USER, EMAIL_PASSWORD)
    mail.select("inbox")
    
    _, data = mail.search(None, "ALL")
    latest_email_id = data[0].split()[-1]
    _, msg_data = mail.fetch(latest_email_id, "(RFC822)")
    
    raw_email = msg_data[0][1]
    msg = email.message_from_bytes(raw_email)
    
    subject = msg["Subject"]
    sender = msg["From"]
    body = ""

    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True).decode()
    else:
        body = msg.get_payload(decode=True).decode()

    return sender, subject, body

def extract_email_and_message(body, sender):
    #print("Sender",sender)
    if sender == "Formspree <noreply@formspree.io>":
        # Normalize line breaks to avoid mismatches
        body = body.replace("\r\n", "\n")  # Standardizing newlines
        print("Raw body content:\n", body)

        # Extract email using regex
        email_pattern = r"email:\s*(.+)"
        email_match = re.search(email_pattern, body)

        # Extract message using string methods (regex din't work for some reason)
        message_start = body.find("message:")
        message_end = body.find("Submitted")

        # Store extracted values (handle cases where they might not be found)
        extracted_email = email_match.group(1).strip() if email_match else None
        print(extracted_email)
        extracted_message = body[message_start+9:message_end]
        print(extracted_message)
        if not extracted_message:
            extracted_message = "Not a business message"
    else:
        #print("Sender not recognised")
        extracted_email = " "
        extracted_message = "Not a business message"

    return extracted_email, extracted_message

# Step 2: Informalize message
def informalize_text(text):
    text = re.sub(r"Dear", "Hey", text)  # Basic informal transformation
    text = re.sub(r"Sincerely,", "Cheers,", text)
    return text

# Step 3: Send via WhatsApp
def send_whatsapp_message(phone, message):
    kit.sendwhatmsg_instantly(phone, message)

# Execute script
while True:
    try:
        sender, subject, body = fetch_email()
        sender_email, message = extract_email_and_message(body, sender)
        
        if message != "Not a business message":
            informal_body = informalize_text(message)
            whatsapp_message = f"📩 New Business Email from {sender_email}\n*{subject}*\n{informal_body}"
            print(whatsapp_message)
            send_whatsapp_message("+447895672837", whatsapp_message)  # Replace with your WhatsApp number
        else:
            print("Latest email was not a business message")
            print(body)
            
        time.sleep(60)  # Run every 60 seconds
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(300)  # Wait longer if an error occurs

