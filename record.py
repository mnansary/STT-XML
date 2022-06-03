import streamlit as st
import sounddevice as sd
import wavio

def read_audio(file):
    with open(file, "rb") as audio_file:
        audio_bytes = audio_file.read()
    return audio_bytes

def record(duration=5, fs=48000):
    sd.default.samplerate = fs
    sd.default.channels = 1
    myrecording = sd.rec(int(duration * fs))
    sd.wait(duration)
    return myrecording

def save_record(path_myrecording, myrecording, fs):
    wavio.write(path_myrecording, myrecording, fs, sampwidth=2)
    return None

if st.button(f"record"):
    filename="record"
    rec_state=st.text("started recording")
    duration=5
    fs=48000
    recording=record(duration,fs)
    rec_state.text(f"saving {filename}.mp3")
    rec_path=f"{filename}.mp3"
    save_record(rec_path,recording,fs)
    rec_state.text(f"Done ! saved {filename}.mp3")
    st.audio(read_audio(rec_path))
