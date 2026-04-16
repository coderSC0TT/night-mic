# -*- coding: utf-8 -*-
import sounddevice as sd
import numpy as np
import wave
import tempfile
import os
import pyttsx3

def find_vb_cable_device():
    for i, dev in enumerate(sd.query_devices()):
        name = dev['name'].lower()
        if 'cable input' in name and dev['max_output_channels'] > 0:
            return i
    return None

VB_DEVICE = find_vb_cable_device()
SAMPLE_RATE = 22050

def text_to_speech(text):
    try:
        temp_file = tempfile.mktemp(suffix=".wav")
        engine = pyttsx3.init('sapi5')
        engine.setProperty("rate", 180)
        engine.setProperty("volume", 1.0)
        engine.save_to_file(text, temp_file)
        engine.runAndWait()
        engine.stop()

        with wave.open(temp_file, 'rb') as wf:
            data = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16)
        os.remove(temp_file)
        return data
    except Exception as e:
        print("TTS??:", e)
        return None

def play_audio(data):
    try:
        sd.play(data, samplerate=SAMPLE_RATE, device=VB_DEVICE)
        sd.wait()
    except:
        pass