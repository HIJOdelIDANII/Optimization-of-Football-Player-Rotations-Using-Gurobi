import "./ChooseTeam.css"

export const ChooseTeam = () => {
  const teams = [
    { id: 1, name: "Liverpool", logo: "/images/teams/Liverpool.jpg" },
    { id: 2, name: "Manchester City", logo: "/images/teams/ManchesterCity.jpg" },
    { id: 3, name: "Manchester United", logo: "/images/teams/ManchesterUnited.jpg" },
  ];

  return (
    <div className="choose-team-container">
      <h1 className="title">Choose Your Favorite Team</h1>
      <div className="card-container">
        {teams.map((team) => (
          <div key={team.id} className="team-card">
            <img src={team.logo} alt={`${team.name} Logo`} className="team-logo" />
            <div className="team-name">{team.name}</div>
          </div>
        ))}
      </div>
    </div>
  );
};
