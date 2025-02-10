from aiCallChatbot import *
import pyaudio
import wave

def record_audio(filename, duration=5, sample_rate=16000):
    chunk = 1024  # Record in chunks of 1024 samples
    format = pyaudio.paInt16  # 16 bits per sample
    channels = 1  # Mono
    rate = sample_rate  # Sample rate

    p = pyaudio.PyAudio()

    # Open stream
    stream = p.open(format=format,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk)

    print("Recording...")

    frames = []

    for _ in range(int(rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    print("Recording finished.")

    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(format))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))

if __name__ == "__main__":
    filenames = input("Enter the base path to save all audio: ")
    print("Starting conversation with the chatbot. Say 'Bye' to end the conversation.")
    response_num = 0

    while True:
        response_num += 1
        # Record user input
        input_audio_path = f"{filenames}_user_input_{response_num}.wav"
        record_audio(input_audio_path, duration=5)

        # Transcribe the question
        transcribed_question = transcribe_audio(input_audio_path)
        print(f"User: {transcribed_question}")

        # Check if the user wants to end the conversation
        if transcribed_question.lower() == "bye" or len(transcribed_question) == 0:
            print("Chatbot: Goodbye!")
            break

        # Generate a response
        relevant_answer = find_answer(transcribed_question)
        print(f"Chatbot: {relevant_answer}")

        # Synthesize the response
        output_audio_path = f"{filenames}_chatbot_response_{response_num}.wav"
        synthesize_speech(relevant_answer, output_audio_path)
        print(f"Chatbot response saved to {output_audio_path}")
