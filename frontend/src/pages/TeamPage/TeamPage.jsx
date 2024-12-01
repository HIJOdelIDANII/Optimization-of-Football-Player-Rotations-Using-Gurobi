import { useParams, useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import "./TeamPage.css";
import { Player } from "../../components/Player/Player";

export const TeamPage = () => {
  const { team_name } = useParams();
  const [players, setPlayers] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    fetchPlayers();
  }, []);

  const fetchPlayers = async () => {
    const response = await fetch(`http://127.0.0.1:5000/api/teams/${team_name}/players/`);
    const data = await response.json();
    setPlayers(data.players);
  };

  const goToMatchSetup = () => {
    navigate(`/setup/${team_name}`);
  };

  return (
    <div className="team-page-container">
      <h1 className="team-page-title">{team_name}</h1>
      <div className="players-container">
        {players.map((player) => (
          <Player key={player.id} player={player} />
        ))}
      </div>
      <button className="setup-button" onClick={goToMatchSetup}>
        Go to Match Setup
      </button>
    </div>
  );
};
