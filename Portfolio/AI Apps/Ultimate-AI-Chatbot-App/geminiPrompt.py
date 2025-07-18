#Importing the modules
import vertexai
from vertexai.generative_models import GenerativeModel
import google.auth

credentials, project_id = google.auth.default()

vertexai.init(project="generalpurposeai", location="us-central1")

model = GenerativeModel(model_name="gemini-2.0-flash")

def generate_response(prompt, mode, type_selection, tone):
    """
    Generate a response from the Gemini model based on the provided prompt, mode, type, and tone.
    
    Args:
        prompt (str): The input prompt for the model.
        mode (str): The mode of interaction (e.g., "chat", "text", "code").
        type_selection (str): The type of response expected (e.g., "summary", "detailed").
        tone (str): The tone of the response (e.g., "formal", "casual").
    
    Returns:
        str: The generated response from the model.
    """
    full_prompt = f"{mode}\nYou to are to generate {type_selection}\nYour tone should be {tone}\n\nThis is what the user stated:\n{prompt}"
    responses = model.generate_content(full_prompt, stream=False)
    return responses.text if responses else ""