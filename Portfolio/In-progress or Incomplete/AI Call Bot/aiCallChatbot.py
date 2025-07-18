from google.cloud import speech
from google.cloud import texttospeech as tts
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
from sklearn.utils import resample

# Initialize the clients
speech_client = speech.SpeechClient()
tts_client = tts.TextToSpeechClient()

def get_evaluation_metrics(y_test, y_pred):
    return {
        "accuracy": accuracy_score(y_test, y_pred),
        "classification_report": classification_report(y_test, y_pred)
    }

# Transcribe audio input
def transcribe_audio(audio_path):
    with open(audio_path, 'rb') as audio_file:
        audio_content = audio_file.read()
    audio = speech.RecognitionAudio(content=audio_content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US'
    )
    response = speech_client.recognize(config=config, audio=audio)
    return response.results[0].alternatives[0].transcript if response.results else ""

# Convert text to speech
def synthesize_speech(text, output_file):
    input_text = tts.SynthesisInput(text=text)
    voice = tts.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Wavenet-D",  # Try experimenting with other voices for a more guttural tone
        ssml_gender=tts.SsmlVoiceGender.MALE
    )
    audio_config = tts.AudioConfig(
        audio_encoding=tts.AudioEncoding.MP3,
        pitch=-15.0,  # Lower pitch for a more monstrous tone
        speaking_rate=0.5  # Slower speech for a powerful, deliberate effect
    )
    response = tts_client.synthesize_speech(
        input=input_text,
        voice=voice,
        audio_config=audio_config
    )
    with open(output_file, "wb") as out:
        out.write(response.audio_content)

# Load and preprocess data
data = pd.read_csv('Conversation.csv')

# Downsample the majority class
majority = data[data['answer'] == 'what do you mean?']
minority = data[data['answer'] != 'what do you mean?']
majority_downsampled = resample(majority, replace=False, n_samples=10, random_state=42)
data_balanced = pd.concat([majority_downsampled, minority])

# Filter out classes with fewer than 2 samples
filtered_data = data_balanced.groupby('answer').filter(lambda x: len(x) > 1)

# Stratified split
X_train, X_test, y_train, y_test = train_test_split(
    filtered_data['question'], filtered_data['answer'], test_size=0.35, stratify=filtered_data['answer'], random_state=42
)

# Vectorize text data
vectorizer = TfidfVectorizer(lowercase=True, stop_words='english', max_features=5000, ngram_range=(1, 2))
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Train a Logistic Regression model
model = LogisticRegression(max_iter=1000, class_weight='balanced')
model.fit(X_train_vec, y_train)

# Evaluate on test set
y_pred = model.predict(X_test_vec)

# Function to find the most relevant answer
def find_answer(question_text):
    question_vec = vectorizer.transform([question_text])
    answer_text = model.predict(question_vec)[0]
    return answer_text

if __name__ == "__main__":
    question = input("Enter your question: ")
    answer = find_answer(question)
    print(f"Answer: {answer}")
