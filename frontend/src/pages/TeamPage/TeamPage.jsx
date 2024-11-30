import { useParams ,useNavigate } from "react-router-dom";
import {useState , useEffect} from "react";
import "./TeamPage.css";
import {Player} from "../../components/player/Player.jsx"
export const TeamPage = ()=>{
    const {team_name} = useParams();
    const navigate = useNavigate();
    const [players, setPlayers] = useState([])
    useEffect(()=>{
        fetchPlayers()
    },[])
    const fetchPlayers = async () => {
    try {
      const response = await fetch(
        `http://127.0.0.1:5000/api/teams/${team_name}/players/`
      );
      const data = await response.json();
      setPlayers(data.players);
    } catch (error) {
      console.error("Error fetching players:", error);
    }
  };

    return(
        <div className="team-page-container">
            <h1 className="team-page-title">{team_name}</h1>
            <button className="back-button" onClick={() => navigate("/")}>
                Back to Teams
            </button>
            <div className="players-container">
                {
                    players.map((player) =>
                        (<Player key={player.id} player={player}></Player>)
                    )}
            </div>
        </div>
    )
}