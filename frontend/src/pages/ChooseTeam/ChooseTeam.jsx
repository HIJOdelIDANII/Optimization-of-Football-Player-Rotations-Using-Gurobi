import "./ChooseTeam.css"
import { useNavigate } from "react-router-dom";
import { ModelInfo } from "../../components/modelInfo/ModelInfo.jsx"; // Import the component
export const ChooseTeam = ({teams=[]}) => {
    const navigate = useNavigate()
    return (

        <div className="choose-team-container">

            <h1 className="title">Choose Your Favorite Team</h1>
            {   teams.length> 0 ? (
                <div className="card-container">
                    {teams.map((team) => (
                        <div key={team.id} className="team-card" onClick={()=> navigate(`/teams/${team.team_name}`)}>
                            <img src={team.logo_path} alt={`${team.team_name} Logo`} className="team-logo"/>
                            <div className="team-name">{team.team_name}</div>
                        </div>

                    ))}</div>)
                    :(
                    <p className="no-teams-message">No teams available.</p> )
                    }

        <ModelInfo></ModelInfo>

        </div>
            );
        };
