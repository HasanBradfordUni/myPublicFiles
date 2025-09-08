from aiCallChatbot import *

import pyaudio
import wave

def record_audio(filename, duration=5, sample_rate=16000):
    # Set up parameters
    chunk = 1024  # Record in chunks of 1024 samples
    format = pyaudio.paInt16  # 16 bits per sample
    channels = 1  # Mono
    rate = sample_rate  # Sample rate

    # Initialize PyAudio
    p = pyaudio.PyAudio()

    # Open stream
    stream = p.open(format=format,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk)

    print("Recording...")

    # Initialize array to store frames
    frames = []

    # Record for the given duration
    for _ in range(int(rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()

    print("Recording finished.")

    # Save the recorded data as a WAV file
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(format))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))

print("Before you start the recording, do you want to get the evaluation metrics of the model?")
answer = input("Enter 'yes' or 'no': ")
if answer.lower() == 'yes':
    evaluation_metrics = get_evaluation_metrics(y_test, y_pred)
    print("Evaluation Metrics:\n")
    for metric, value in evaluation_metrics.items():
        print(f"{metric}: {value}")

# Example usage
input_audio_path = input("Enter the path to save the input audio: ")
duration = int(input("Enter the duration of the recording (in seconds): "))
record_audio(input_audio_path, duration)

# Example usage
transcribed_question = transcribe_audio(input_audio_path)
print(f"Transcribed Question: {transcribed_question}")

relevant_answer = find_answer(transcribed_question)
print(f"Relevant Answer: {relevant_answer}")

output_audio_path = input("Enter the path to save the response audio: ")
synthesize_speech(relevant_answer, output_audio_path)
print(f"Saved response to {output_audio_path}")