import "./Player.css";

export const Player = ({ player = {} }) => {
  return (
    <div className="player-card">
      <div className="player-info">
        <img src={player.image_path} alt={`${player.player_name} photo`} />
        <div className="player-hover-info">
          <p>Goals/Game: {player.potential_goals_per_game}</p>
          <p>Physicality: {player.physicality}</p>
          <p>Nationality: {player.nationality}</p>
        </div>
      </div>
      <div className="player-name">{player.player_name}</div>
    </div>
  );
};
