# 🎧 Audio Mix Analyzer

**AI-powered audio analysis with in-depth engineering insights**

Audio Mix Analyzer is a full-stack application that allows users to upload an audio track—optionally along with a reference track—and receive a comprehensive technical analysis powered by signal-processing algorithms and expert-level AI evaluation.

This tool is built for producers, mixing engineers, musicians, and content creators who want **objective mix metrics** combined with **professional, AI-refined engineering feedback**.

---

## 🚀 Features

### 🔍 1. Audio Feature Extraction

The backend uses scientific DSP libraries to compute detailed audio metrics such as:

- RMS, peak level, dynamic range
- Spectral centroid & rolloff
- Loudness & energy curves
- Frequency distribution & timbre analysis
- Stereo width & correlation
- Tempo, rhythm & transient density
- And many more…

---

### 🎚️ 2. Optional Reference Track Comparison

Users can upload a second “reference track” to compare:

- Loudness match
- Tonal balance
- Dynamic behavior
- Frequency spectrum alignment
- Stereo image profile

Perfect for recreating the mix style of professional tracks.

---

### 🤖 3. AI-Generated Expert Mix Report

After extracting features, the backend sends structured audio data to a specialized LLM.

The AI returns:

- A well-formatted JSON report
- Clear mix categories (EQ, compression, stereo, loudness, etc.)
- Genre-aware technical insights
- Professional “mix engineer style” explanations
- Practical suggestions for improving the mix

---

## 🧠 Tech Stack

### Backend

- **FastAPI**
- **NumPy**
- **Librosa**
- **Groq API / LLM**
- **ProcessPoolExecutor**

### Frontend

- **React**
- **TypeScript**
- **Fetch API**

---

## 📦 How It Works

1. User uploads the main audio track
2. _(Optional)_ user uploads a reference track
3. Backend processes audio → extracts features via Librosa
4. Features are packaged into a structured schema
5. LLM generates a detailed engineering-style mix report
6. Frontend displays the analysis in clean, selectable categories

---

## 🎯 Use Cases

- Producers checking mix quality
- Audio engineers comparing a mix with a reference
- Students learning mixing & mastering principles
- Quick analysis for demos and studio sessions
- Automated mix review tools

---
