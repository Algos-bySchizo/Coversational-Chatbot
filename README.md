# 🎙️ SpeechAgent — Conversational AI with Voice & Text I/O

A fully conversational AI chatbot built with **LangGraph**, **Groq**, and **Whisper** that supports both speech and text input/output with persistent memory across sessions.

---

## ✨ Features

- 🎤 **Speech Input** — speak to the agent, Groq's Whisper API transcribes it instantly
- ⌨️ **Text Input** — type your messages like a regular chatbot
- 🔊 **Speech Output** — agent speaks responses back using Google TTS (gTTS)
- 📝 **Text Output** — responses printed cleanly to terminal
- 🧠 **Persistent Memory** — conversation history saved to JSON, loaded back on next run
- 🔄 **Back and Forth Chat** — full multi-turn conversation support
- 🗑️ **Clear History** — wipe conversation and start fresh anytime
- 🚪 **Graceful Exit** — type 'exit' to quit cleanly

---

## 🏗️ Architecture

This project uses **LangGraph** to build a stateful, graph-based conversational pipeline. Each step in the conversation is a **node** in the graph, connected by **edges** that define the flow.

```
START
  ↓
[get_input]        ← asks: speech or text? exit? clear?
  ↓
[should_continue]  ← conditional routing based on user choice
  ↓          ↓           ↓
[END]    [get_input]  [handle_input]
(exit)   (clear)      (normal flow)
              ↓
        [handle_transcribe]  ← whisper transcribes if speech
              ↓
        [handle_generate]    ← Groq LLM generates response
              ↓
        [handle_output]      ← speaks or prints response
              ↓
        [get_input]          ← loops back for next message
```

### LangGraph Concepts Used

| Concept | How We Use It |
|---|---|
| `StateGraph` | defines the overall graph structure |
| `State (TypedDict)` | shared memory passed between all nodes |
| `add_messages` | appends messages to history instead of replacing |
| `add_node()` | registers each function as a graph node |
| `add_edge()` | connects nodes with fixed paths |
| `add_conditional_edges()` | routes dynamically based on user input |
| `compile()` | validates and locks the graph structure |
| `stream()` | runs the graph step by step |

---

## 📁 Project Structure

```
SpeechAgent/
  ├── main.py          # LangGraph graph — connects all nodes
  ├── state.py         # shared state definition (TypedDict)
  ├── listener.py      # records audio from microphone
  ├── transcriber.py   # sends audio to Groq Whisper API
  ├── llm.py           # sends messages to Groq Llama LLM
  ├── speaker.py       # converts text to speech via gTTS
  ├── history.py       # saves/loads conversation to JSON
  ├── .env.example     # environment variable template
  ├── requirements.txt # project dependencies
  └── .gitignore       # files excluded from git
```

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| [LangGraph](https://langchain-ai.github.io/langgraph/) | graph-based agent framework |
| [Groq](https://console.groq.com) | LLM inference (Llama 3.1) + Whisper transcription |
| [gTTS](https://gtts.readthedocs.io) | Google Text to Speech |
| [sounddevice](https://python-sounddevice.readthedocs.io) | microphone audio recording |
| [scipy](https://scipy.org) | saving recorded audio as .wav |
| [python-dotenv](https://pypi.org/project/python-dotenv/) | loading environment variables |

---

## ⚙️ Setup

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/SpeechAgent.git
cd SpeechAgent
```

### 2. Create a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
# on Windows: venv\Scripts\activate
```

### 3. Install system dependencies
```bash
sudo apt-get install portaudio19-dev mpg123 ffmpeg
# portaudio19-dev = required for microphone recording
# mpg123 = plays generated speech audio
# ffmpeg = audio processing
```

### 4. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 5. Set up your API key
```bash
cp .env.example .env
# then edit .env and add your Groq API key
```

Your `.env` file should look like:
```
API=gsk_your_groq_api_key_here
```

Get your free Groq API key at [console.groq.com](https://console.groq.com)

### 6. Run the agent
```bash
python3 main.py
```

---

## 💬 Usage

```
🎙️  SpeechAgent Started!
Type 'exit' to quit, 'clear' to reset history

How would you like to talk? (s/t) / 'exit' / 'clear': 
```

| Command | What it does |
|---|---|
| `s` | speech input — speak into your microphone |
| `t` | text input — type your message |
| `exit` | quit the program |
| `clear` | wipe conversation history and start fresh |

After each response:
```
Speak or print response? (s/t):
```
| Command | What it does |
|---|---|
| `s` | agent speaks the response out loud |
| `t` | response printed to terminal |

---

## 🧩 How Each File Works

**`state.py`** — defines the shared state dictionary that all nodes read from and write to:
```python
class State(TypedDict):
    messages: Annotated[list, add_messages]  # conversation history
    input_mode: str       # "speech" or "text"
    output_mode: str      # "speech" or "text"
    transcription: str    # what user said/typed
    response: str         # LLM's reply
    audio_path: str       # path to recorded .wav file
```

**`listener.py`** — records audio from microphone using `sounddevice`. Press Enter to stop recording. Uses threading to record in background while waiting for Enter key.

**`transcriber.py`** — sends recorded `.wav` file to Groq's Whisper API and returns transcribed text. Runs on Groq's servers — no local processing needed.

**`llm.py`** — sends full conversation history to Groq's Llama 3.1 8B model and returns the response. Handles LangGraph message objects by converting them to plain dicts.

**`speaker.py`** — converts text to speech using gTTS (Google's TTS), speeds it up using ffmpeg, plays with mpg123, then deletes the temporary file.

**`history.py`** — saves conversation to `convo_history.json` after every message. Loads it back on next run so the agent remembers previous sessions.

**`main.py`** — builds and runs the LangGraph graph. Defines all nodes, connects them with edges, handles routing logic, and streams the graph execution.

---

## 🔑 Environment Variables

| Variable | Description |
|---|---|
| `API` | Your Groq API key — get it free at console.groq.com |

---

## 📝 Notes

- Conversation history is stored in `convo_history.json` — this file is gitignored and stays local
- The agent remembers conversations across sessions until you type `clear`
- Speech recognition requires an internet connection (uses Groq's Whisper API)
- Text to speech requires an internet connection (uses Google's gTTS)
- Microphone recording works offline

---

## 🙏 Acknowledgements

- [LangGraph](https://langchain-ai.github.io/langgraph/) by LangChain
- [Groq](https://groq.com) for fast LLM inference and Whisper API
- [Google TTS](https://gtts.readthedocs.io) for natural voice output