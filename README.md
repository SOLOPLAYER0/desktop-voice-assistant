# AI Desktop Voice Assistant (Alice)

An end-to-end AI-powered desktop voice assistant built using Python that integrates Speech-to-Text (STT), NLP preprocessing, LLM + Retrieval-Augmented Generation (RAG), and Text-to-Speech (TTS) to enable intelligent, voice-driven system interaction.

The assistant supports conversational responses, system automation, and real-time voice command execution in a continuous interactive loop.

---

## Features

- Speech-to-Text using `speech_recognition`
- Text-to-Speech using `pyttsx3`
- LLM + RAG-based reasoning for conversational responses
- NLP preprocessing pipeline:
  - Text cleaning
  - Intent detection
  - Keyword extraction
  - Sentence segmentation
- Desktop automation:
  - Open/close applications
  - Volume control
  - Browser automation
  - System monitoring (CPU & battery)
- Wikipedia-based information retrieval and summarization
- Modular architecture for future LLM integration

---

## System Architecture

```text
User Voice Input
        ↓
Speech-to-Text (STT)
        ↓
NLP Preprocessing
        ↓
Query Routing
   ↙                ↘
System Commands     LLM + RAG
   ↓                    ↓
Execution           Response Generation
        ↓
Text-to-Speech (TTS)
        ↓
Voice Output
```
## Tech Stack

- **Language:** Python 3.x  
- **Speech Processing:** `speech_recognition`, `pyttsx3`  
- **LLM & RAG Integration:** Custom reasoning pipeline  
- **Web Scraping:** `BeautifulSoup`, `requests`  
- **Automation:** `PyAutoGUI`, `os`, `psutil`  
- **Other Libraries:** `wikipedia`, `re`, `datetime`, `webbrowser`

## Installation

### Clone the Repository

```bash
git clone https://github.com/yourusername/ai-voice-assistant.git
cd ai-voice-assistant
```
### Install Dependencies
```bash
pip install -r requirements.txt
```
## Usage

### Run the assistant:
```bash
python main.py
```

### The assistant will:

- Greet the user
- Continuously listen for voice commands
- Execute system commands or generate intelligent responses

### Example Commands

- Open calculator
- Increase volume
- Search Google for machine learning
- Tell me about Artificial Intelligence
-Check system status

### Future Improvements

- Wake-word detection (e.g., “Hey Alice”)
- Offline STT using Whisper
- Advanced LLM integration (Llama / Mistral)
- Memory-based personalization
- Cross-platform support

### Project Motivation

- This project demonstrates the integration of:
- Speech processing
- Natural Language Processing
- Retrieval-Augmented Generation
- System automation
- Real-time interactive AI pipelines

## 📌 Author

Shashank Pratyush