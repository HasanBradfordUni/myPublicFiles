from flask import Flask, render_template, request, jsonify
import vertexai
from vertexai.generative_models import GenerativeModel
import google.auth

app = Flask(__name__)

# Initialize Vertex AI
credentials, project_id = google.auth.default()
vertexai.init(project="generalpurposeai", location="us-central1")
model = GenerativeModel(model_name="gemini-1.5-flash")

@app.route('/')
def home():
    return render_template('ai-chat.html')

@app.route('/chat', methods=['POST'])
def chat():
    prompt = request.form['prompt']
    if prompt:
        responses = model.generate_content(prompt, stream=True)
        response_text = ''.join([response.text for response in responses])
        return jsonify({'response': response_text})
    return jsonify({'response': 'No prompt provided'})

if __name__ == '__main__':
    app.run('localhost', 6922)