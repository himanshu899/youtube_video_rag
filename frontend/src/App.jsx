import React, { useState } from "react";
import Chat from "./components/Chat";
import Game from "./components/Game";
import "./App.css";

const API_URL = "http://localhost:8000";

function App() {
  const [videoId, setVideoId] = useState("");
  const [question, setQuestion] = useState("");
  const [chatHistory, setChatHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [loadLoading, setLoadLoading] = useState(false);
  const [transcriptLoaded, setTranscriptLoaded] = useState(false);
  const [error, setError] = useState("");
  const [theme, setTheme] = useState(
    window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light"
  );
  const [showGame, setShowGame] = useState(false);

  React.useEffect(() => {
    document.body.setAttribute("data-theme", theme);
  }, [theme]);

  const loadTranscript = async () => {
    setError("");
    setTranscriptLoaded(false);
    setLoadLoading(true);
    setChatHistory([]); // Clear chat when loading new video
    const res = await fetch(`${API_URL}/transcript`, {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({video_id: videoId}),
    });
    const data = await res.json();
    setLoadLoading(false);
    if (data.success) setTranscriptLoaded(true);
    else setError(data.message);
  };

  const askQuestion = async () => {
    setLoading(true);
    setShowGame(true);
    setError("");
    const res = await fetch(`${API_URL}/ask`, {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({video_id: videoId, question}),
    });
    const data = await res.json();
    setLoading(false);
    setShowGame(false); // Hide game popup when response received
    if (data.success) {
      // Print full answer to console
      console.log("Full LLM answer:", data.answer);
      // Trim <think>...</think> blocks and show only main response
      let trimmed = data.answer.replace(/<think>[\s\S]*?<\/think>/gi, "").trim();
      // Also trim 'Answer:' if present
      if (trimmed.includes("Answer:")) {
        trimmed = trimmed.split("Answer:")[1].trim();
      } else {
        trimmed = trimmed.split("\n\n")[0].trim();
      }
      setChatHistory([...chatHistory, {question, answer: trimmed, time: new Date().toLocaleTimeString()}]);
      setQuestion("");
    } else {
      setError(data.message);
    }
  };

  return (
    <div className={`meta-chat-root ${theme}`}>
      <div className="meta-chat-card">
        <header className="meta-chat-header">
          <img src="/vite.svg" alt="logo" className="meta-chat-logo" />
          <h1> YouTube RAG</h1>
          <button
            aria-label="Toggle theme"
            className="meta-chat-btn theme-toggle-btn"
            onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
            style={{marginLeft: "auto"}}
          >
            {theme === "dark" ? "🌞" : "🌙"}
          </button>
        </header>
        <div className="meta-chat-controls">
          <div className="meta-chat-videoid-card">
            <input
              type="text"
              placeholder="Enter YouTube Video ID"
              value={videoId}
              onChange={e => setVideoId(e.target.value)}
              className="meta-chat-input meta-chat-videoid-input"
              disabled={loadLoading}
            />
            <button 
              onClick={loadTranscript} 
              className="meta-chat-btn meta-chat-load-btn"
              disabled={loadLoading || !videoId}
            >
              {loadLoading ? <span className="meta-chat-spinner" /> : "Load"}
            </button>
          </div>
        </div>
        {error && <div className="meta-chat-error">{error}</div>}
        {transcriptLoaded && (
          <>
            <div className="meta-chat-window">
              <Chat history={chatHistory} />
              <div id="meta-chat-bottom" />
            </div>
            <form
              className="meta-chat-input-bar"
              onSubmit={e => {
                e.preventDefault();
                if (question) askQuestion();
              }}
            >
              <input
                type="text"
                placeholder="Ask a question about the video"
                value={question}
                onChange={e => setQuestion(e.target.value)}
                className="meta-chat-input"
                disabled={loading}
              />
              <button
                type="submit"
                className="meta-chat-btn"
                disabled={loading || !question}
              >
                Send
              </button>
            </form>
            {showGame && (
              <div className="meta-game-modal-overlay">
                <div className="meta-game-modal">
                  <button className="meta-game-close" onClick={() => setShowGame(false)} aria-label="Close game">✖</button>
                  <Game />
                </div>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}

export default App;