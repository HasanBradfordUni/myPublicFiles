from speechToText import transcribe_audio
from txetToSpeech import synthesize_speech
import pyaudio
import wave

def listen_and_speak():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 48000
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    while True:
        #data = stream.read(CHUNK)
        #with open("audio.wav", "wb") as f:
            #f.write(data)
        text = transcribe_audio("audio.wav")
        print("User:", text)
        speech = synthesize_speech(text)
        with open("output.mp3", "wb") as f:
            f.write(speech)
        play_audio("output.mp3")
        print("Bot:", text)

def play_audio(audio_file):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True)
    wf = wave.open(audio_file, "rb")
    data = wf.readframes(CHUNK)
    while data:
        stream.write(data)
        data = wf.readframes(CHUNK)
    stream.stop_stream()
    stream.close()
    audio.terminate()

listen_and_speak()
