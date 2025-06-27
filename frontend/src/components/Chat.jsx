import React, { useRef, useEffect } from "react";
import "./../App.css";

export default function Chat({ history }) {
  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [history]);

  return (
    <div className="meta-chat-messages">
      {history.map((chat, idx) => (
        <React.Fragment key={idx}>
          <div className="meta-chat-row user">
            <div className="meta-chat-bubble user">
              <span className="meta-chat-avatar">🧑</span>
              <span className="meta-chat-text">{chat.question}</span>
              <span className="meta-chat-time-bubble">{chat.time || ""}</span>
            </div>
          </div>
          <div className="meta-chat-row bot">
            <div className="meta-chat-bubble bot">
              <span className="meta-chat-avatar">🤖</span>
              <span className="meta-chat-text">{chat.answer}</span>
              <span className="meta-chat-time-bubble">{chat.time || ""}</span>
            </div>
          </div>
        </React.Fragment>
      ))}
      <div ref={chatEndRef} />
    </div>
  );
}