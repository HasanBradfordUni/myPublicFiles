#Importing the modules
import vertexai
from vertexai.generative_models import GenerativeModel
import google.auth

credentials, project_id = google.auth.default()

vertexai.init(project="generalpurposeai", location="us-central1")

model = GenerativeModel(model_name="gemini-1.0-pro")

while True:
    prompt = input("Enter a prompt for the Ai to process: ")
    if prompt != "":
      responses = model.generate_content(prompt, stream=True)
      for response in responses:
          print(response.text)
    else:
        exit()
