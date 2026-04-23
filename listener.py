import sounddevice as sd
import scipy.io.wavfile as wav
import numpy as np
import threading

def record_audio(sample_rate = 44100):
    
    print('\nGo ahead I\'m listening..... Press enter to send when you\'re done\n')
    
    frames = []
    
    stop_event = threading.Event()
    
    
    def callback(indata, _f, _t, _status):
        
        frames.append(indata.copy())
        
        if stop_event.is_set():
            raise sd.CallbackStop
        
    with sd.InputStream(samplerate=sample_rate, channels=1, dtype="int16" ,callback=callback):
            input()
            stop_event.set()

    audio = np.concatenate(frames, axis = 0)

    wav.write("audio.wav", sample_rate, audio)

    print('Recording Done!')
    return "audio.wav"
    