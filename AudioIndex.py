import pyaudio

def list_audio_devices():
    p = pyaudio.PyAudio()
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        print(f"Index: {info['index']}, Name: {info['name']}, Input channels: {info['maxInputChannels']}, Output channels: {info['maxOutputChannels']}, Sample rate: {info['defaultSampleRate']}")

    p.terminate()

if __name__ == "__main__":
    list_audio_devices()