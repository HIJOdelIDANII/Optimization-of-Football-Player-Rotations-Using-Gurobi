import { useState } from "react";
import { useParams } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";

export const MatchSetup = () => {
  const { team_name } = useParams();
  const [gamesNumber, setGamesNumber] = useState(1);
  const [teamName, setTeamName] = useState("");
  const [difficultyLevel, setDifficultyLevel] = useState(null);
  const [numGamesAdded, setNumGamesAdded] = useState(0);
  const [opponentsList, setOpponentsList] = useState([]);
  const [disabledButton, setDisabledButton] = useState(false);
  const [stats, setStats] = useState(null);

  const handleChange = (event) => {
    setDifficultyLevel(parseFloat(event.target.value));
  };

  const addOpponent = (opponent, diff) => {
    setOpponentsList([...opponentsList, { opponent: opponent, difficulty: diff }]);
  };

  const fetchData = async (myData) => {
    const url = `http://127.0.0.1:5000/api/optimise/${team_name}/`;
    const options = {
      method: "POST",
      headers: {
        "Content-type": "application/json",
      },
      body: JSON.stringify(myData),
    };
    const response = await fetch(url, options);
    const data = await response.json();
    console.log(data);
    setStats(data);
  };

  const Submit = async () => {
    const myJsonData = {
      numberMatches: gamesNumber,
      matchesChosen: {},
    };
    for (let i = 0; i < opponentsList.length; i++) {
      myJsonData.matchesChosen[i.toString()] = opponentsList[i];
    }
    fetchData(myJsonData);
  };

  const verifyVariables4Add = () => {
    if (teamName === "" || difficultyLevel === null) {
      alert("Please fill all inputs");
    } else {
      setNumGamesAdded((prev) => {
        const updatedNumGames = prev + 1;
        if (updatedNumGames === parseInt(gamesNumber, 10)) {
          setDisabledButton(true);
        }
        return updatedNumGames;
      });
      addOpponent(teamName, difficultyLevel);
      setTeamName("");
      setDifficultyLevel(null);
    }
  };

  const verifyVariable4submit = () => {
    if (numGamesAdded < parseInt(gamesNumber, 10)) {
      alert(`You only added ${numGamesAdded} opponents. Please add ${gamesNumber - numGamesAdded}`);
    } else {
      Submit();
      setTeamName("");
      setDifficultyLevel(null);
      setGamesNumber(1);
    }
  };

  return (
    <div className="container mt-4 text-white">
      <h2 className="bg-primary text-center p-2 rounded">Match Setup</h2>

      {/* Form Section */}
      <div className="row">
        <div className="col-md-6">
          <div className="form-group">
            <label htmlFor="games_number">Choose Number of Games</label>
            <input
              id="games_number"
              type="number"
              min="1"
              max="38"
              value={gamesNumber}
              className="form-control text-black"
              onChange={(e) => setGamesNumber(parseInt(e.target.value, 10))}
            />
          </div>
          <div className="form-group">
            <label htmlFor="team_name">Team Name</label>
            <input
              id="team_name"
              type="text"
              value={teamName}
              className="form-control text-black"
              onChange={(e) => setTeamName(e.target.value)}
            />
          </div>
        </div>

        <div className="col-md-6">
          <h5 className="bg-secondary text-center p-2 rounded">Match Difficulty</h5>
          <div className="form-check">
            <input
              id="easy"
              type="radio"
              name="difficulty"
              value="0.5"
              className="form-check-input"
              checked={difficultyLevel === 0.5}
              onChange={handleChange}
            />
            <label className="form-check-label" htmlFor="easy">
              Easy
            </label>
          </div>
          <div className="form-check">
            <input
              id="medium"
              type="radio"
              name="difficulty"
              value="1.0"
              className="form-check-input"
              checked={difficultyLevel === 1.0}
              onChange={handleChange}
            />
            <label className="form-check-label" htmlFor="medium">
              Medium
            </label>
          </div>
          <div className="form-check">
            <input
              id="hard"
              type="radio"
              name="difficulty"
              value="1.5"
              className="form-check-input"
              checked={difficultyLevel === 1.5}
              onChange={handleChange}
            />
            <label className="form-check-label" htmlFor="hard">
              Hard
            </label>
          </div>
        </div>
      </div>

      <div className="mt-3 text-center">
        <button
          disabled={disabledButton}
          className="btn btn-primary me-2"
          onClick={verifyVariables4Add}
        >
          Add Opponent
        </button>
        <button className="btn btn-success" onClick={verifyVariable4submit}>
          Submit
        </button>
      </div>

      {/* Statistics Section */}
      {stats && (
        <div>
          <div className="card bg-dark mt-5 p-4 text-white">
            <h2 className="bg-danger text-center p-2 rounded">Statistics</h2>
            <h4>Total Goals Scored: {stats.total_goals}</h4>
            <h5>Player Statistics</h5>
            <ul className="list-group">
              {stats.player_statistics.map((playerStat, index) => (
                <li
                  key={index}
                  className="list-group-item bg-dark text-white border-secondary"
                >
                  {playerStat.player}: {playerStat.matches_played} matches
                </li>
              ))}
            </ul>
          </div>

          {/* Matches Section */}
          <h2 className="bg-primary text-center mt-5 p-2 rounded">Lineups</h2>
          <div className="row">
            {stats.lineups.map((lineup, index) => (
              <div className="col-md-4 mb-4" key={index}>
                <div className="card bg-dark text-white border-primary">
                  <div className="card-body">
                    <h5 className="card-title">
                      Match {lineup.match}: {lineup.opponent}
                    </h5>
                    <p className="card-text">Goals: {lineup.goals}</p>
                    <p className="card-text">
                      Players: {lineup.players.join(", ")}
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
