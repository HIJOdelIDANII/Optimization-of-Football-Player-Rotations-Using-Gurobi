from gurobipy import Model, GRB, quicksum
from flask import jsonify  # Use jsonify for structured JSON responses

def bestThree(number_of_games, difficulty_list, physicality_list, goals_list):
    players = range(6)  # 6 attackers
    matches = range(number_of_games)  # Number of matches
    G = goals_list  # Goals per game for each player
    P = physicality_list  # Maximum consecutive matches based on physicality
    C = difficulty_list  # Match difficulty

    m = Model("Football Rotation with Synergy and Match Complexity")
    m.setParam('OutputFlag', 0)

    # Decision variables
    x = m.addVars(players, matches, vtype=GRB.BINARY, name="x")  # Player selection

    # Team size constraint
    for t in matches:
        m.addConstr(quicksum(x[i, t] for i in players) == 3, name=f"TeamSize_Match{t}")

    # Consecutive match constraint
    for i in players:
        for t in range(len(matches) - P[i]):  # Adjust window size based on physicality
            m.addConstr(
                quicksum(x[i, t + k] for k in range(P[i] + 1)) <= P[i],
                name=f"Consecutive_Player{i}_Match{t}"
            )

    # Rest key players for easier matches
    for t in matches:
        if C[t] == 0.5:  # Easy match
            m.addConstr(quicksum(x[i, t] for i in players if G[i] <= 0.5) >= 2, name=f"Rest_Strong_Match{t}")

    # Objective function
    goal_part = quicksum(C[t] * G[i] * x[i, t] for i in players for t in matches)
    m.setObjective(goal_part, GRB.MAXIMIZE)

    # Solve the model
    m.optimize()

    # Prepare JSON response
    match_lineups = []
    player_counts = [0] * len(players)  # To track total appearances for each player
    total_goals = 0  # To calculate total goals for the season

    for t in matches:
        match_lineup = {"match": t + 1, "players": [], "goals": 0}
        match_goals = 0  # Goals for this match
        for i in players:
            if x[i, t].x > 0.5:  # If player is selected
                match_lineup["players"].append(f"Player {i + 1}")
                player_counts[i] += 1
                match_goals += G[i]  # Add the player's goals to the match total
        match_lineup["goals"] = match_goals
        match_lineups.append(match_lineup)
        total_goals += match_goals  # Add match goals to season total

    # Player statistics
    player_statistics = [
        {"player": f"Player {i + 1}", "matches_played": player_counts[i]}
        for i in players
    ]

    # Create the JSON response
    response = {
        "lineups": match_lineups,
        "player_statistics": player_statistics,
        "total_goals": total_goals
    }

    return jsonify(response)
