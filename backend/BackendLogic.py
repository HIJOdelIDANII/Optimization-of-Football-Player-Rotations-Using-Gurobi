from gurobipy import Model, GRB, quicksum
from flask import jsonify  # Use jsonify for structured JSON responses

def bestThree(number_of_games, difficulty_list, physicality_list, goals_list, players_names_list, oponents_list):
    players = players_names_list  # Player names
    matches = range(number_of_games)  # Number of matches
    G = goals_list  # Goals per game for each player
    P = physicality_list  # Maximum consecutive matches based on physicality
    C = difficulty_list  # Match difficulty

    m = Model("Football Rotation with Synergy and Match Complexity")
    m.setParam('OutputFlag', 0)

    # Decision variables
    x = m.addVars(players, matches, vtype=GRB.BINARY, name="x")  # Use player names as keys

    # Team size constraint
    for t in matches:
        m.addConstr(quicksum(x[player, t] for player in players) == 3, name=f"TeamSize_Match{t}")

    # Consecutive match constraint
    for i, player in enumerate(players):
        for t in range(number_of_games - P[i]):  # Adjust window size based on physicality
            m.addConstr(
                quicksum(x[player, t + k] for k in range(P[i] + 1)) <= P[i],
                name=f"Consecutive_{player}_Match{t}"
            )

    # Rest key players for easier matches
    for t in matches:
        if C[t] == 0.5:  # Easy match
            m.addConstr(quicksum(x[player, t] for player in players if G[players.index(player)] <= 0.5) >= 2, name=f"Rest_Strong_Match{t}")

    # Objective function
    goal_part = quicksum(C[t] * G[players.index(player)] * x[player, t] for player in players for t in matches)
    m.setObjective(goal_part, GRB.MAXIMIZE)

    # Solve the model
    m.optimize()

    # Prepare JSON response
    match_lineups = []
    player_counts = {player: 0 for player in players}  # To track total appearances for each player
    total_goals = 0  # To calculate total goals for the season

    for t in matches:
        match_lineup = {"match": t + 1, "players": [], "goals": 0, "opponent": oponents_list[t]}
        match_goals = 0  # Goals for this match

        for player in players:
            if x[player, t].x > 0.5:  # If player is selected
                match_lineup["players"].append(player)
                player_counts[player] += 1
                match_goals += G[players.index(player)]  # Add the player's goals to the match total
        match_lineup["goals"] = match_goals
        match_lineups.append(match_lineup)
        total_goals += match_goals  # Add match goals to season total

    # Player statistics
    player_statistics = [
        {"player": player, "matches_played": player_counts[player]}
        for player in players
    ]

    # Create the JSON response
    response = {
        "lineups": match_lineups,
        "player_statistics": player_statistics,
        "total_goals": total_goals
    }

    return jsonify(response)
