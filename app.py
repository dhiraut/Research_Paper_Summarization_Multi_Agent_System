import os
import tempfile
from typing import List

import fitz  # PyMuPDF
import requests
from transformers import pipeline
from gtts import gTTS
import streamlit as st

# ---------- CONFIG ----------
def summarize_text(text: str) -> str:
    if not text.strip():
        return "Summary not available (empty text)."

    try:
        # Truncate long text safely
        if len(text) > 2000:
            text = text[:2000]

        summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
        result = summarizer(text, max_length=200, min_length=30, do_sample=False)

        if result and isinstance(result, list) and 'summary_text' in result[0]:
            return result[0]['summary_text']
        return "Summary not available (model did not return text)."
    except Exception as e:
        return f"Summary failed: {str(e)}"

def extract_text_from_pdf(pdf_path: str) -> str:
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def classify_topic(text: str, topics: List[str]) -> str:
    if not text.strip():
        return "Unknown (no text extracted)"
    if not topics:
        return "Unknown (no topics provided)"

    classifier = pipeline("zero-shot-classification", model="valhalla/distilbart-mnli-12-3")
    result = classifier(text[:1000], candidate_labels=topics)

    if 'labels' in result and isinstance(result['labels'], list) and len(result['labels']) > 0:
        return result['labels'][0]
    return "Unknown (classification failed)"

def generate_audio(text: str, output_path: str):
    try:
        tts = gTTS(text)
        tts.save(output_path)
    except Exception as e:
        raise RuntimeError(f"Audio generation failed: {str(e)}")

# ---------- STREAMLIT UI ----------
st.set_page_config(page_title="Research Paper Summarizer", layout="centered")
st.title("📄 AI Research Paper Summarizer")

st.markdown("""
Upload a research paper (PDF) and a list of topics. The app will:
1. Extract and summarize the paper
2. Classify it into a topic
3. Generate an audio summary 🎧
""")

with st.form("upload_form"):
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
    topic_input = st.text_input("Enter comma-separated topics")
    submitted = st.form_submit_button("Summarize and Generate Audio")

if submitted and uploaded_file and topic_input:
    with st.spinner("Processing paper..."):
        try:
            temp_dir = tempfile.mkdtemp()
            file_path = os.path.join(temp_dir, uploaded_file.name)

            with open(file_path, "wb") as f:
                f.write(uploaded_file.read())

            text = extract_text_from_pdf(file_path)
            st.info(f"Extracted text length: {len(text)} characters")

            if not text.strip():
                st.error("❌ No text could be extracted from the PDF. Try another file.")
            else:
                topic_list = [t.strip() for t in topic_input.split(",") if t.strip()]
                classified_topic = classify_topic(text, topic_list)
                summary = summarize_text(text)

                st.markdown(f"### 🧠 Classified Topic: `{classified_topic}`")
                st.markdown("### ✍️ Summary:")
                st.write(summary)

                audio_path = os.path.join(temp_dir, "summary.mp3")
                generate_audio(summary, audio_path)

                st.markdown("### 🔊 Audio Summary")
                st.audio(audio_path)
                st.success("Done! Audio summary is ready.")

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
