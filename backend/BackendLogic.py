from gurobipy import Model, GRB, quicksum
from flask import jsonify  # Use jsonify for structured JSON responses

def bestThree(number_of_games, difficulty_list, physicality_list, goals_list, players_names_list, oponents_list):
    players = players_names_list  # 6 attackers
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
        m.addConstr(quicksum(x[i, t] for i in range(len(players))) == 3, name=f"TeamSize_Match{t}")

    # Consecutive match constraint
    for i in range(len(players)):
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
    goal_part = quicksum(C[t] * G[i] * x[i, t] for i in range(len(players)) for t in matches)
    m.setObjective(goal_part, GRB.MAXIMIZE)

    # Solve the model
    m.optimize()

    # Prepare JSON response
    match_lineups = []
    player_counts = [0] * len(players)  # To track total appearances for each player
    total_goals = 0  # To calculate total goals for the season
    j=0
    for t in matches:
        match_lineup = {"match": t + 1, "players": [], "goals": 0 ,"oponent":oponents_list[j]}
        j=j+1
        match_goals = 0  # Goals for this match
        k=0
        for i in players:

            if x[k, t].x > 0.5:  # If player is selected
                match_lineup["players"].append(f"{i}")
                player_counts[k] += 1
                match_goals += G[k]  # Add the player's goals to the match total
            k=k+1
        match_lineup["goals"] = match_goals
        match_lineups.append(match_lineup)
        total_goals += match_goals  # Add match goals to season total

    # Player statistics
    e=0
    player_statistics = []
    k=0
    for i in players:
        player_statistics.append(
            {"player": f"Player {i}", "matches_played": player_counts[k]}
        )
        k=k+1

    # Create the JSON response
    response = {
        "lineups": match_lineups,
        "player_statistics": player_statistics,
        "total_goals": total_goals
    }

    return jsonify(response)
