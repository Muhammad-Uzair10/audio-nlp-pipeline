# 🎵 Audio NLP Pipeline

Real-time ambient audio analysis using Whisper and advanced NLP techniques for detecting aggressive language, trigger terms, and behavioral patterns.

## 🚀 Features
- **Speech-to-Text**: Powered by OpenAI Whisper (tiny/medium models)
- **Voice Activity Detection**: Filters noise and silence
- **Aggressive Language Detection**: Identifies threatening phrases
- **Trigger Term Recognition**: Flags emergency/help keywords
- **Sentiment Analysis**: Multi-model sentiment scoring
- **Speaker Diarization**: Who said what (optional)
- **Pattern Learning**: Adapts to new patterns over time
- **Webhook Integration**: Real-time alerts
- **Production Ready**: Docker, FastAPI, PostgreSQL

## 🛠️ Tech Stack
- **ASR**: Whisper (OpenAI)
- **NLP**: spaCy, Transformers, TextBlob
- **Backend**: FastAPI + Uvicorn
- **Database**: SQLite/PostgreSQL
- **Task Queue**: Celery + Redis
- **Deployment**: Docker + Docker Compose

## 📦 Installation

### Prerequisites
- Python 3.8+
- FFmpeg
- Redis (for background tasks)

### Setup
```bash
# Clone repository
git clone https://github.com/USERNAME/audio-nlp-pipeline.git
cd audio-nlp-pipeline

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm
