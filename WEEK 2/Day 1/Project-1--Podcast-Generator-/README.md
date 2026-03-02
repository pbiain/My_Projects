# 🎙️ Podcast Studio

> An automated AI-powered podcast generation system that transforms text, notes, PDFs, and other content sources into professional audio podcasts.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Pipeline Architecture](#pipeline-architecture)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## Overview

Podcast Studio is a mini-project built as part of the Ironhack AI Bootcamp (Week 2). Inspired by tools like Google NotebookLM, it automates the end-to-end process of turning raw content — notes, PDFs, articles, or plain text — into structured audio podcasts using LLMs and Text-to-Speech APIs.

The system follows a clean three-step pipeline:

```
Data Input → LLM Transformation → Audio Generation
```

---

## Features

- 📄 **Multi-source input** — supports `.txt`, `.md`, `.json`, and raw text
- 🤖 **AI script generation** — uses LLMs to transform content into engaging podcast scripts
- 🔑 **Key point extraction** — automatically identifies and highlights the most important ideas
- 🔊 **Text-to-speech audio output** — generates high-quality audio with multiple voice options
- 🎛️ **Multiple podcast styles** — conversational, educational, interview, and storytelling
- 🌐 **Gradio web interface** — simple, user-friendly UI accessible via browser
- 🔗 **Audio merging** — combines multiple audio chunks into a single podcast file

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.8+ |
| Frontend | Gradio |
| LLM | OpenAI / Anthropic API |
| Text-to-Speech | OpenAI TTS / ElevenLabs / Google Cloud TTS |
| Speech-to-Text (optional) | OpenAI Whisper |
| Vector DB (optional) | Pinecone |
| ML Framework | PyTorch + Transformers |

---

## Project Structure

```
Project-1--Podcast-Generator/
├── main.py                    # Main application & Gradio interface
├── data_processor.py          # Handles file ingestion and validation
├── llm_processor.py           # LLM API calls for script generation
├── tts_generator.py           # Text-to-speech audio generation
├── concat.txt                 # Audio file concatenation helper
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
├── project.ipynb              # Jupyter notebook for experimentation
└── supplements_scorecard_notes.txt  # Sample input data
```

---

## Installation

### Prerequisites

- Python 3.8 or higher
- An API key for an LLM provider (OpenAI, Anthropic, etc.)
- An API key for a TTS provider (OpenAI, ElevenLabs, etc.)

### Steps

1. **Clone the repository**

```bash
git clone <your-repo-url>
cd Project-1--Podcast-Generator
```

2. **Create and activate a virtual environment** (recommended)

```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here  # optional
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here  # optional
```

---

## Usage

### Launch the Gradio Web Interface

```bash
python main.py
```

This will start a local server and open the Gradio UI in your browser. A shareable public link will also be printed to the console.

### From File

1. Navigate to the **"From File"** tab
2. Upload a `.txt`, `.md`, or `.json` file
3. Select a **podcast style** (conversational, educational, interview, storytelling)
4. Select a **voice** (nova, shimmer, echo, alloy, onyx, fable)
5. Click **"Generate Podcast"**

### From Text

1. Navigate to the **"From Text"** tab
2. Paste your raw content into the text area
3. Choose your style and voice preferences
4. Click **"Generate Podcast"**

### Python API (Programmatic Use)

```python
from main import PodcastStudio

studio = PodcastStudio()

# From a file
result = studio.create_podcast_from_file(
    file_path="my_notes.txt",
    style="educational",
    voice="nova"
)

# From raw text
result = studio.create_podcast_from_text(
    text="Your content here...",
    style="conversational",
    voice="shimmer"
)

print(result["script"])       # Generated podcast script
print(result["audio_files"])  # Paths to audio output files
```

---

## Pipeline Architecture

```
┌──────────────────┐
│   Input Source   │  (.txt / .md / .json / raw text)
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  DataProcessor   │  Reads, cleans & validates content
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  LLMProcessor    │  Generates podcast script + extracts key points
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  TTSGenerator    │  Converts script to audio chunks
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│   Merged Audio   │  Final .mp3 podcast output
└──────────────────┘
```

---

## Configuration

| Parameter | Options | Default | Description |
|-----------|---------|---------|-------------|
| `style` | `conversational`, `educational`, `interview`, `storytelling` | `conversational` | Tone and format of the generated script |
| `voice` | `nova`, `shimmer`, `echo`, `alloy`, `onyx`, `fable` | `nova` | TTS voice used for audio generation |

---

## Contributing

Contributions are welcome! To get started:

1. Fork the repository
2. Create a new feature branch: `git checkout -b feature/your-feature-name`
3. Make your changes and commit: `git commit -m "Add your feature"`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Open a Pull Request

Please make sure your code follows existing style conventions and includes appropriate comments.

---

## License

This project is intended for educational purposes as part of the Ironhack AI Bootcamp. All rights reserved by the respective author.

---

## Contact

Built with 🎧 during **Ironhack AI Bootcamp — Week 2, Day 1**

For questions or feedback, please reach out via the course platform or open an issue in this repository.
