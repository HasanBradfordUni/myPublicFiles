from google.cloud import texttospeech as tts

def synthesize_speech(text):
    client = tts.TextToSpeechClient()
    synthesis_input = tts.SynthesisInput(text=text)
    voice = tts.VoiceSelectionParams(
        language_code="en-UK",
        ssml_gender=tts.SsmlVoiceGender.NEUTRAL
    )
    audio_config = tts.AudioConfig(
        audio_encoding=tts.AudioEncoding.MP3
    )
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    return response.audio_content
