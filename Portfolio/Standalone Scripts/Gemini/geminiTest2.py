import vertexai
from vertexai.generative_models import GenerativeModel
import google.auth
from tkinter import *
from tkinterhtml import HtmlFrame
import markdown

try:
    credentials, project_id = google.auth.default()
    print("Google Auth successful")
except Exception as e:
    print(f"Google Auth failed: {e}")

try:
    vertexai.init(project="generalpurposeai", location="us-central1")
    print("Vertex AI initialized")
except Exception as e:
    print(f"Vertex AI initialization failed: {e}")

try:
    model = GenerativeModel(model_name="gemini-1.0-pro")
    print("Model loaded")
except Exception as e:
    print(f"Model loading failed: {e}")

class ChatbotWindow(Tk):
    def __init__(self):
        super().__init__()
        self.title('Chatbot Interface')

        self.conversation_html = ""

        self.conversation = HtmlFrame(self, horizontal_scrollbar="auto")
        self.conversation.pack(expand=True, fill='both')

        self.user_input = Entry(self)
        self.user_input.pack(side='left', expand=True, fill='x')

        self.send_button = Button(self, text='Send', command=self.send_message)
        self.send_button.pack(side='right')

    def send_message(self):
        prompt = self.user_input.get()
        if prompt:
            try:
                print("User input received:", prompt)
                plaintext_prompt = f"{prompt}\n\nPlease generate a response in markdown."
                print("Plaintext prompt created:", plaintext_prompt)

                # Temporarily remove model interaction
                # responses = model.generate_content(plaintext_prompt, stream=True)
                responses = ["This is a test response."]  # Mock response for testing

                user_message = f"<p><b>User:</b> {prompt}</p>"
                self.conversation_html += user_message
                self.conversation.set_content(self.conversation_html)
                print("User message added to conversation")

                for response in responses:
                    html_response = markdown.markdown(response)
                    chatbot_message = f"<p><b>Chatbot:</b> {html_response}</p>"
                    self.conversation_html += chatbot_message
                    self.conversation.set_content(self.conversation_html)
                    print("Chatbot response added to conversation")

                self.user_input.delete(0, 'end')
                print("User input cleared")
            except Exception as e:
                print(f"Error during message processing: {e}")

    def get_conversation_text(self):
        return self.conversation_html

if __name__ == "__main__":
    try:
        window = ChatbotWindow()
        window.mainloop()
    except Exception as e:
        print(f"Error in main loop: {e}")
