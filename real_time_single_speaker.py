import pvkoala
from pvrecorder import PvRecorder
import pyaudio
import numpy as np
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

access_key = os.getenv("ACCESS_KEY")

# Create Koala instance
koala = pvkoala.create(access_key)
frame_length = koala.frame_length

# Start recorder
recorder = PvRecorder(device_index=-1, frame_length=frame_length)
recorder.start()

# Set up PyAudio for playback
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=koala.sample_rate,
                output=True)

try:
    print("Processing in near real-time. Press Ctrl+C to stop.")
    while True:
        pcm = recorder.read()
        enhanced_pcm = koala.process(pcm)
        stream.write(np.array(enhanced_pcm, dtype=np.int16).tobytes())

except KeyboardInterrupt:
    pass
finally:
    stream.stop_stream()
    stream.close()
    p.terminate()

    recorder.stop()
    recorder.delete()
    koala.delete()
    print("\nStopped.")