import streamlit as st
import whisper
import tempfile
import os

st.set_page_config(page_title="Whisper Transcriber", layout="centered")

st.title("🎙️ Local Whisper Transcriber (Offline & Free)")
st.write("Upload an audio file and get a transcribed `.txt` file. Runs 100% locally using open-source Whisper.")

# Load model once and cache it
@st.cache_resource
def load_model():
    return whisper.load_model("medium")

model = load_model()

uploaded_file = st.file_uploader("📂 Upload an audio file", type=["mp3", "wav", "m4a", "flac"])

if uploaded_file:
    with st.spinner("Transcribing... This may take a while..."):
        # Save uploaded file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name

        result = model.transcribe(tmp_path)
        transcript = result["text"]

        # Save transcript to .txt
        txt_path = tmp_path + "_transcript.txt"
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(transcript)

        os.remove(tmp_path)  # Clean up audio file

        st.success("✅ Transcription complete!")
        st.text_area("📄 Transcript Preview", transcript, height=200)
        st.download_button("⬇️ Download Transcript", transcript, file_name="transcript.txt")

