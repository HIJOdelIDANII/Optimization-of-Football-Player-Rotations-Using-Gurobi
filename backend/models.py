from config import db
from sqlalchemy import text


class Team(db.Model):
    __tablename__ = 'teams'

    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(100), nullable=False, unique=False)
    logo_url = db.Column(db.String(255), nullable=True)  # Path or URL to the team logo
    players = db.relationship('Player', backref='team', lazy=True)

    def to_json(self):
        return {
            "id": self.id,
            "team_name": self.team_name,
            "logo_url": self.logo_url,
            "players": [player.to_json() for player in self.players]
        }


class Player(db.Model):
    __tablename__ = 'players'

    id = db.Column(db.Integer, primary_key=True)
    player_name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    nationality = db.Column(db.String(50), nullable=False)
    potential_goals_per_game = db.Column(db.Float, nullable=False)
    image_path = db.Column(db.String(255), nullable=True)
    physicality = db.Column(db.Integer, nullable=False)  # New attribute
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)

    def to_json(self):
        return {
            "id": self.id,
            "player_name": self.player_name,
            "age": self.age,
            "nationality": self.nationality,
            "potential_goals": self.potential_goals,
            "image_url": self.image_url,
            "physicality": self.physicality,
            "team_id": self.team_id
        }


players_data = [
    # Liverpool
    {"player_name": "Mohamed Salah", "age": 32, "nationality": "Egypt", "potential_goals_per_game": 0.7, "physicality": 3, "image_path": "./assets/images/players/mohamed_salah.jpg", "team_name": "Liverpool"},
    {"player_name": "Darwin Núñez", "age": 25, "nationality": "Uruguay", "potential_goals_per_game": 0.6, "physicality": 2, "image_path": "./assets/images/players/darwin_nunez.jpg", "team_name": "Liverpool"},
    {"player_name": "Diogo Jota", "age": 27, "nationality": "Portugal", "potential_goals_per_game": 0.5, "physicality": 2, "image_path": "./assets/images/players/diogo_jota.jpg", "team_name": "Liverpool"},
    {"player_name": "Luis Díaz", "age": 27, "nationality": "Colombia", "potential_goals_per_game": 0.4, "physicality": 1, "image_path": "./assets/images/players/luis_diaz.jpg", "team_name": "Liverpool"},
    {"player_name": "Cody Gakpo", "age": 25, "nationality": "Netherlands", "potential_goals_per_game": 0.3, "physicality": 1, "image_path": "./assets/images/players/cody_gakpo.jpg", "team_name": "Liverpool"},
    {"player_name": "Roberto Firmino", "age": 33, "nationality": "Brazil", "potential_goals_per_game": 0.25, "physicality": 1, "image_path": "./assets/images/players/roberto_firmino.jpg", "team_name": "Liverpool"},

    # Manchester City
    {"player_name": "Erling Haaland", "age": 24, "nationality": "Norway", "potential_goals_per_game": 1.2, "physicality": 3, "image_path": "./assets/images/players/erling_haaland.jpg", "team_name": "ManchesterCity"},
    {"player_name": "Phil Foden", "age": 24, "nationality": "England", "potential_goals_per_game": 0.4, "physicality": 2, "image_path": "./assets/images/players/phil_foden.jpg", "team_name": "ManchesterCity"},
    {"player_name": "Jack Grealish", "age": 29, "nationality": "England", "potential_goals_per_game": 0.35, "physicality": 2, "image_path": "./assets/images/players/jack_grealish.jpg", "team_name": "ManchesterCity"},
    {"player_name": "Julian Álvarez", "age": 24, "nationality": "Argentina", "potential_goals_per_game": 0.3, "physicality": 2, "image_path": "./assets/images/players/julian_alvarez.jpg", "team_name": "ManchesterCity"},
    {"player_name": "Bernardo Silva", "age": 30, "nationality": "Portugal", "potential_goals_per_game": 0.25, "physicality": 1, "image_path": "./assets/images/players/bernardo_silva.jpg", "team_name": "ManchesterCity"},
    {"player_name": "Riyad Mahrez", "age": 34, "nationality": "Algeria", "potential_goals_per_game": 0.2, "physicality": 1, "image_path": "./assets/images/players/riyad_mahrez.jpg", "team_name": "ManchesterCity"},

    # Manchester United
    {"player_name": "Marcus Rashford", "age": 27, "nationality": "England", "potential_goals_per_game": 0.8, "physicality": 3, "image_path": "./assets/images/players/marcus_rashford.jpg", "team_name": "ManchesterUnited"},
    {"player_name": "Anthony Martial", "age": 29, "nationality": "France", "potential_goals_per_game": 0.4, "physicality": 2, "image_path": "./assets/images/players/anthony_martial.jpg", "team_name": "ManchesterUnited"},
    {"player_name": "Jadon Sancho", "age": 24, "nationality": "England", "potential_goals_per_game": 0.35, "physicality": 2, "image_path": "./assets/images/players/jadon_sancho.jpg", "team_name": "ManchesterUnited"},
    {"player_name": "Antony", "age": 24, "nationality": "Brazil", "potential_goals_per_game": 0.3, "physicality": 1, "image_path": "./assets/images/players/antony.jpg", "team_name": "ManchesterUnited"},
    {"player_name": "Mason Greenwood", "age": 23, "nationality": "England", "potential_goals_per_game": 0.25, "physicality": 1, "image_path": "./assets/images/players/mason_greenwood.jpg", "team_name": "ManchesterUnited"},
    {"player_name": "Alejandro Garnacho", "age": 20, "nationality": "Argentina", "potential_goals_per_game": 0.2, "physicality": 1, "image_path": "./assets/images/players/alejandro_garnacho.jpg", "team_name": "ManchesterUnited"},
]


def clear_database():
    db.session.query(Player).delete()
    db.session.query(Team).delete()
    db.session.commit()

    if db.engine.name == 'sqlite':
        result = db.session.execute(
            text("SELECT name FROM sqlite_master WHERE type='table' AND name='sqlite_sequence'")
        )
        if result.fetchone():
            db.session.execute(text("DELETE FROM sqlite_sequence WHERE name='teams'"))
            db.session.execute(text("DELETE FROM sqlite_sequence WHERE name='players'"))
            db.session.commit()

    print("Database cleared and primary keys reset successfully!")


def populate_database():
    clear_database()
    teams = {team_name: Team(team_name=team_name, logo_url=f"./assets/images/teams/{team_name.replace(' ', '_').lower()}.png") for team_name in set(player['team_name'] for player in players_data)}
    db.session.add_all(teams.values())
    db.session.commit()

    for player_data in players_data:
        team = teams[player_data['team_name']]
        player = Player(
            player_name=player_data['player_name'],
            age=player_data['age'],
            nationality=player_data['nationality'],
            potential_goals_per_game=player_data['potential_goals_per_game'],
            physicality=player_data['physicality'],  # New field
            image_path=player_data['image_path'],
            team_id=team.id
        )
        db.session.add(player)
    db.session.commit()
