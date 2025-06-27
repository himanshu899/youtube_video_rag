# YouTube Video RAG (Retrieval-Augmented Generation) App

A full-stack app to ask questions about any YouTube video using its transcript and an LLM (Ollama DeepSeek-R1).  
**Backend:** FastAPI (Python)  
**Frontend:** React + Vite

---

## Features

- Enter a YouTube video ID, load its transcript, and build a semantic index.
- Ask questions about the video; answers are generated using RAG (retrieval-augmented generation) with context from the transcript.
- Fun number guessing game while you wait for answers!
- Modern, responsive UI with light/dark mode.

---

## Requirements

- **Python 3.9+**
- **Node.js 18+** and **npm**
- [Ollama](https://ollama.com/) running locally with the `deepseek-r1:1.5b` model pulled
- (Optional) [FAISS](https://github.com/facebookresearch/faiss) for vector storage (handled via `langchain_community`)

---

## Setup Instructions

### 1. Clone the Repository

```sh
git clone <your-repo-url>
cd youtube_video_rag
```

---

### 2. Backend Setup (FastAPI)

#### a. Create a Python virtual environment

```sh
python3 -m venv .venv
source .venv/bin/activate
```

#### b. Install dependencies

```sh
pip install fastapi uvicorn youtube-transcript-api langchain langchain-community langchain-ollama
```

#### c. Start Ollama and pull the model

Make sure Ollama is running locally:

```sh
ollama serve
ollama pull deepseek-r1:1.5b
```

#### d. Run the backend server

```sh
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

---

### 3. Frontend Setup (React + Vite)

```sh
cd frontend
npm install
npm run dev
```

The frontend will be available at [http://localhost:5173](http://localhost:5173) (default Vite port).

---

## Usage

1. **Start the backend** (`uvicorn ...`) and ensure Ollama is running with the required model.
2. **Start the frontend** (`npm run dev`).
3. Open the frontend in your browser.
4. Enter a YouTube video ID (e.g., `Gfr50f6ZBvo`), click **Load**.
5. Once loaded, ask any question about the video.
6. Play the number guessing game while waiting for answers!

---

## Project Structure

```
youtube_video_rag/
├── backend/
│   └── main.py         # FastAPI backend (API endpoints)
├── frontend/
│   ├── src/            # React source code
│   ├── package.json
│   └── ...
├── sample.py           # Streamlit demo (optional)
├── youtube_rag.py      # Standalone script for RAG pipeline (optional)
└── README.md           # (You are here)
```

---

## API Endpoints

- `POST /transcript`  
  **Body:** `{ "video_id": "<YouTube ID>" }`  
  Loads and indexes the transcript.

- `POST /ask`  
  **Body:** `{ "video_id": "<YouTube ID>", "question": "<your question>" }`  
  Returns an answer from the LLM using RAG.

---

## Notes

- For development, CORS is open. Restrict in production!
- Ollama and the required model must be running locally.
- Only public YouTube videos with English transcripts are supported.

---

## Troubleshooting

- **No captions available:** Some videos do not have transcripts or captions enabled.
- **Ollama errors:** Ensure Ollama is running and the model is pulled.
- **Port conflicts:** Change ports in `vite.config.js` or `uvicorn` if needed.

---

## Credits

- [LangChain](https://github.com/langchain-ai/langchain)
- [Ollama](https://ollama.com/)
- [YouTube Transcript API](https://github.com/jdepoix/youtube-transcript-api)
- [FAISS](https://github.com/facebookresearch/faiss)

---

## License

MIT License