import React, { useState } from "react";
import "./ModelInfo.css";

export const ModelInfo = () => {
  const [showInfo, setShowInfo] = useState(false);

  const toggleInfo = () => {
    setShowInfo(!showInfo);
  };

  return (
    <div className={`choose-team-container ${showInfo ? "blur-background" : ""}`}>
      {showInfo && (
        <div className="info-banner">
          <h2>
            <span className="typewriter">About the Model</span>
          </h2>
          <p className="info-text">

              This model optimizes team performance by balancing player physicality and match difficulty.

              It ensures optimal player rotation across matches while protecting player health and maximizing goals.

          </p>
          <div>
            <button className="close-info-button" onClick={toggleInfo}>
              Close
            </button>
            <a
              className="pdf-button"
              href="/FootballRotationModel.pdf"  // Replace with your PDF file path
              target="_blank"
              rel="noopener noreferrer"
            >
              View PDF
            </a>
          </div>
        </div>
      )}

      <button className="info-button" onClick={toggleInfo}>
        About the Model
      </button>
    </div>
  );
};
