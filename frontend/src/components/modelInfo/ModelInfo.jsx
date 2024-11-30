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
          <h2>About the Model</h2>
          <p>
            This model optimizes team performance by balancing player physicality and
            match difficulty. It ensures optimal player rotation
            across matches while protecting player health and maximizing goals.
          </p>
          <button className="close-info-button" onClick={toggleInfo}>
            Close
          </button>
        </div>
      )}

      <button className="info-button" onClick={toggleInfo}>
        About the Model
      </button>

    </div>
  );
};
