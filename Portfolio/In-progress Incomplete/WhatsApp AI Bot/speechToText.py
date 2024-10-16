from google.cloud import speech_v1 as speech

def transcribe_audio(audio_file):
    client = speech.SpeechClient()
    with open(audio_file, "rb") as audio_file:
        content = audio_file.read()
    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=48000,
        language_code="en-UK",
    )
    response = client.recognize(config=config, audio=audio)
    return response.results[0].alternatives[0].transcript
