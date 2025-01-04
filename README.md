# Real-Time Audio Enhancement with pvkoala and PvRecorder

This project demonstrates a real-time audio enhancement application using the **pvkoala** library for noise suppression and the **PvRecorder** library for capturing audio from multiple input devices. The application supports playback of enhanced audio and can mix audio from multiple sources.

## Features
- **Near real-time noise suppression** using pvkoala.
- **Support for multiple input audio devices.**
- **Playback of enhanced audio** using PyAudio.
- **Easy device selection** with input device listing.

## Prerequisites
1. **Python 3.7 or later**
2. **Required Python libraries:**
   - pvkoala
   - pvrecorder
   - pyaudio
   - numpy
   - python-dotenv

## Installation

1. **Install Required Libraries:**
   ```bash
   pip install pvkoala pvrecorder pyaudio numpy python-dotenv
   ```

2. **Set Up API Key:**
   Create a `.env` file in the root of your project and add your `ACCESS_KEY`:
   ```
   ACCESS_KEY=your_access_key_here
   ```

3. **Hardware Requirements:**
   - Microphone(s) for audio input
   - Speakers or headphones for audio playback

## Usage

1. **List Available Input Devices:**
   Run the script to list audio input devices. Replace the indices in `device_indices` with your desired devices.
   ```python
   list_input_devices()
   ```

2. **Start Real-Time Audio Processing:**
   Run the main script to start capturing audio, processing it with pvkoala, and playing the enhanced output:
   ```bash
   python main.py
   ```
   Press `Ctrl+C` to stop the application.

## How It Works

1. **Initialization:**
   - Loads the `ACCESS_KEY` from the `.env` file.
   - Initializes pvkoala for noise suppression.
   - Lists available input devices for user selection.

2. **Audio Capture:**
   - Uses PvRecorder to capture audio frames from specified devices.

3. **Audio Processing:**
   - Enhances captured audio frames with pvkoala.
   - Mixes audio from multiple sources and prevents clipping.

4. **Playback:**
   - Plays the enhanced audio in real time using PyAudio.

## Code Highlights

**Device Selection**
```python
def list_input_devices():
    p = pyaudio.PyAudio()
    for i in range(p.get_device_count()):
        device_info = p.get_device_info_by_index(i)
        if device_info.get('maxInputChannels') > 0:
            print(f"Index {i}: {device_info.get('name')}")
    p.terminate()
```

**Real-Time Audio Processing**
```python
def process_audio():
    while True:
        mixed_pcm = np.zeros(frame_length, dtype=np.float32)
        for recorder in recorders:
            pcm = recorder.read()
            enhanced_pcm = koala.process(pcm)
            mixed_pcm += np.array(enhanced_pcm, dtype=np.float32)
        mixed_pcm = (mixed_pcm / len(recorders)).astype(np.int16)
        stream.write(mixed_pcm.tobytes())
```

## Notes
- Replace `device_indices` with indices corresponding to your preferred input devices.