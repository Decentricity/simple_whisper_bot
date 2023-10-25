import pyaudio
import wave
import whisper
import warnings

# Function to record audio
def record_audio(filename, duration=5):
    p = pyaudio.PyAudio()

    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=16000,
                    input=True,
                    frames_per_buffer=1024)

    print("Recording...")

    frames = []

    for i in range(0, int(16000 / 1024 * duration)):
        data = stream.read(1024)
        frames.append(data)

    print("Finished recording.")

    # Stop the stream and close PyAudio
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save the recorded data to a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(16000)
    wf.writeframes(b''.join(frames))
    wf.close()

# Suppress warnings
warnings.filterwarnings('ignore')

# Record audio and save to 'audio.wav'
record_audio('audio.wav')

# Load the Whisper model
model = whisper.load_model("base")

# Transcribe the audio
result = model.transcribe("audio.wav")

# Extract and print the transcribed text
transcription = result.get('text', '')
print(transcription)
