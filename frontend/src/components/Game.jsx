import React, { useState } from "react";

export default function Game() {
  const [target, setTarget] = useState(() => Math.floor(Math.random() * 20) + 1);
  const [guess, setGuess] = useState("");
  const [message, setMessage] = useState("Guess a number between 1 and 20!");
  const [attempts, setAttempts] = useState(0);
  const [gameOver, setGameOver] = useState(false);

  const handleGuess = () => {
    const num = parseInt(guess, 10);
    if (isNaN(num) || num < 1 || num > 20) {
      setMessage("Please enter a valid number between 1 and 20.");
      return;
    }
    setAttempts(attempts + 1);
    if (num === target) {
      setMessage(`🎉 Correct! The number was ${target}. Attempts: ${attempts + 1}`);
      setGameOver(true);
    } else if (num < target) {
      setMessage("Too low! Try again.");
    } else {
      setMessage("Too high! Try again.");
    }
    setGuess("");
  };

  const handleRestart = () => {
    setTarget(Math.floor(Math.random() * 20) + 1);
    setGuess("");
    setMessage("Guess a number between 1 and 20!");
    setAttempts(0);
    setGameOver(false);
  };

  return (
    <div className="meta-game-popup-content">
      <h2 className="meta-game-title">🎮 Quick Number Game</h2>
      <div className="meta-game-subtitle">Guess a number between 1 and 20 while you wait for the answer!</div>
      <div className="meta-chat-row bot">
        <div className="meta-chat-bubble bot" style={{width: "100%", flexDirection: "column", alignItems: "flex-start", boxShadow: 'none', border: 'none', background: 'transparent'}}>
          <span style={{marginBottom: 8}}>{message}</span>
          {!gameOver && (
            <div style={{display: "flex", gap: 8, width: "100%"}}>
              <input
                type="number"
                min="1"
                max="20"
                value={guess}
                onChange={e => setGuess(e.target.value)}
                className="meta-chat-input"
                style={{width: 80, marginRight: 0}}
                onKeyDown={e => { if (e.key === "Enter") handleGuess(); }}
                autoFocus
              />
              <button
                onClick={handleGuess}
                className="meta-chat-btn"
                style={{minWidth: 80}}
              >
                Guess
              </button>
            </div>
          )}
          {gameOver && (
            <button
              onClick={handleRestart}
              className="meta-chat-btn"
              style={{marginTop: 10, minWidth: 120, background: "#10b981"}}
            >
              Play Again
            </button>
          )}
        </div>
      </div>
    </div>
  );
}