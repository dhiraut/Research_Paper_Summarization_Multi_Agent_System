# 🧠 Research Paper Summarization System

This project is a **Streamlit-based AI summarizer** that extracts, analyzes, and summarizes research papers from uploaded PDFs. It also classifies them into relevant topics and generates **audio summaries** using Text-to-Speech.

---

## 🎬 Demonstration

Watch a quick walkthrough of how to use the app on Hugging Face Spaces:

[![Demonstration Video](https://img.youtube.com/vi/placeholder/0.jpg)](https://github.com/user-attachments/assets/a144319a-7f26-44cb-8cac-6c4a54ceb08a)

📽️ [Click here to watch the demo](https://github.com/user-attachments/assets/a144319a-7f26-44cb-8cac-6c4a54ceb08a)

🚀 **Try it live on Hugging Face Spaces:** [rbbist/Research_Paper_Summarization_Multi_Agent_System](https://huggingface.co/spaces/rbbist/Research_Paper_Summarization_Multi_Agent_System)

---

## 🔧 Setup Instructions

### ▶️ Local Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/dhiraut/Research_Paper_Summarization_Multi_Agent_System.git
   cd Research_Paper_Summarization_Multi_Agent_System
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app:**
   ```bash
   streamlit run app.py
   ```

### ▶️ Hugging Face Spaces

- Upload `app.py`, `requirements.txt`, and this `README.md`.
- Set up the app as a **Streamlit Space** (not Gradio or Docker).
- You're good to go!

---

## 🏗️ System Architecture

The system is built as a **monolithic Streamlit application** that encapsulates all logic within a single file (`app.py`). It does the following:

1. Accepts PDF uploads and topic inputs.
2. Extracts text from the PDF using PyMuPDF.
3. Summarizes the extracted content using a transformer-based summarization model.
4. Classifies the paper into one of the provided topics using zero-shot learning.
5. Converts the generated summary into speech using gTTS.
6. Displays the text and plays back the audio within the UI.

---

## 🤖 Multi-Agent Design and Coordination Approach

Though implemented in a single file for simplicity, the logic mimics a **multi-agent system**, with modular components:

| Agent Role                  | Function                                                                 |
|----------------------------|--------------------------------------------------------------------------|
| 📄 PDF Processing Agent     | Extracts text from uploaded research papers using PyMuPDF.               |
| 🧠 Topic Classifier Agent   | Classifies paper content using `zero-shot-classification`.               |
| ✍️ Summarizer Agent         | Uses transformer models to generate concise summaries.                   |
| 🎙️ Audio Generation Agent  | Converts summary text into audio with `gTTS`.                            |

Each logical module acts independently and communicates via function calls, allowing future conversion into fully decoupled microservices or agent-based components.

---

## 📚 Paper Processing Methodology

- **PDF Parsing:** PyMuPDF is used to extract readable text from academic papers.
- **Text Preprocessing:** Text is truncated (to ~2000 characters) for model efficiency and to prevent overloading Hugging Face-hosted spaces.
- **Summarization:** A lightweight model (`sshleifer/distilbart-cnn-12-6`) provides short, coherent summaries.
- **Topic Classification:** Topics entered by the user are matched against paper content using `valhalla/distilbart-mnli-12-3`.

---

## 🔊 Audio Generation Implementation

- **Library:** [gTTS (Google Text-to-Speech)](https://pypi.org/project/gTTS/)
- **Workflow:**
  1. Summary is passed to gTTS.
  2. Speech is synthesized into an MP3 file.
  3. The MP3 is returned to Streamlit and embedded in the UI.
- **Limitations:** Requires internet access; not fully offline-compatible.

---

## ⚠️ Limitations and Future Improvements

### ❌ Limitations

- **Model limitations:** Hugging Face Spaces have limited memory; heavy models like GPT or BART-large may crash.
- **No cross-paper synthesis:** The system only handles one paper at a time.
- **TTS requires internet:** gTTS does not work offline.
- **No persistent storage:** Summaries/audio are not saved or archived.

### ✅ Future Improvements

- Replace gTTS with an **offline TTS engine** like `Coqui` or `pyttsx3`.
- Integrate **cross-paper synthesis** and trend summarization.
- Use **background processing** or async queues (e.g., Celery) for scalability.
- Deploy separate **backend microservices** for each agent role.
- Add **search functionality** via arXiv API or Semantic Scholar.
- Incorporate **DOI and URL parsing** to ingest external papers.

---

## 💡 Tech Stack

- Python 3.10+
- Streamlit
- Hugging Face Transformers
- PyMuPDF
- gTTS

---

## 🧠 Author Notes

This project is intended as a prototype for research analysis via LLMs. It focuses on core logic, interpretability, and deployability within a lightweight, serverless container like Hugging Face Spaces.
