import pvkoala
from pvrecorder import PvRecorder
import pyaudio
import numpy as np
import threading
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

access_key = os.getenv("ACCESS_KEY")

# Initialize Koala instance
koala = pvkoala.create(access_key)
frame_length = koala.frame_length
sample_rate = koala.sample_rate


def list_input_devices():
    p = pyaudio.PyAudio()
    print("Available Audio Input Devices:")
    for i in range(p.get_device_count()):
        device_info = p.get_device_info_by_index(i)
        if device_info.get('maxInputChannels') > 0:
            print(f"Index {i}: {device_info.get('name')}")
    p.terminate()

# Call the function to list devices
list_input_devices()

# Specify the device indices you want to use
device_indices = [0, 2]  # Replace with your actual device indices

# Create PvRecorder instances for each input device
recorders = []
for idx in device_indices:
    recorder = PvRecorder(device_index=idx, frame_length=frame_length)
    recorder.start()
    recorders.append(recorder)

# Set up PyAudio for playback
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=sample_rate,
                output=True)

# Function to read from all recorders and process audio
def process_audio():
    print("Processing in near real-time. Press Ctrl+C to stop.")
    try:
        while True:
            mixed_pcm = np.zeros(frame_length, dtype=np.float32)
            for recorder in recorders:
                pcm = recorder.read()
                enhanced_pcm = koala.process(pcm)
                mixed_pcm += np.array(enhanced_pcm, dtype=np.float32)
            # Prevent clipping by normalizing
            mixed_pcm = mixed_pcm / len(recorders)
            # Convert to int16
            mixed_pcm = mixed_pcm.astype(np.int16)
            stream.write(mixed_pcm.tobytes())
    except KeyboardInterrupt:
        pass
    # Cleanup
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

        for recorder in recorders:
            recorder.stop()
            recorder.delete()
        koala.delete()
        print("\nStopped.")


# Run the audio processing in the main thread
process_audio()