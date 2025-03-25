from ortools.linear_solver import pywraplp
from flask import jsonify  # For structured JSON responses

def bestThree(number_of_games, difficulty_list, physicality_list, goals_list, players_names_list, oponents_list):
    players = players_names_list  # Player names
    matches = range(number_of_games)  # Number of matches
    G = goals_list  # Goals per game for each player
    P = physicality_list  # Maximum consecutive matches based on physicality
    C = difficulty_list  # Match difficulty

    # Create the solver instance using CBC
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        return jsonify({"error": "Solver not created."})

    # Decision variables: x[player, t] are binary variables indicating if player is selected in match t.
    x = {}
    for player in players:
        for t in matches:
            x[player, t] = solver.BoolVar(f'x_{player}_{t}')

    # Constraint: Team size must equal 3 for each match.
    for t in matches:
        solver.Add(sum(x[player, t] for player in players) == 3)

    # Constraint: Consecutive match constraint for each player based on their physicality limit.
    for i, player in enumerate(players):
        for t in range(number_of_games - P[i]):
            solver.Add(sum(x[player, t + k] for k in range(P[i] + 1)) <= P[i])

    # Constraint: For easy matches (difficulty == 0.5), at least 2 players with low goals (<= 0.5) must be rested.
    for t in matches:
        if C[t] == 0.5:
            solver.Add(sum(x[player, t] for player in players if G[players.index(player)] <= 0.5) >= 2)

    # Objective: Maximize total weighted goals across all matches.
    # The weight is given by the match difficulty and the player's goal value.
    objective = solver.Objective()
    for player in players:
        for t in matches:
            coeff = C[t] * G[players.index(player)]
            objective.SetCoefficient(x[player, t], coeff)
    objective.SetMaximization()

    # Solve the model
    status = solver.Solve()
    if status != pywraplp.Solver.OPTIMAL and status != pywraplp.Solver.FEASIBLE:
        return jsonify({"error": "No optimal solution found."})

    # Prepare JSON response
    match_lineups = []
    player_counts = {player: 0 for player in players}  # To track total appearances for each player
    total_goals = 0  # To calculate total goals for the season

    for t in matches:
        match_lineup = {"match": t + 1, "players": [], "goals": 0, "opponent": oponents_list[t]}
        match_goals = 0  # Goals for this match

        for player in players:
            # Check if the player is selected in match t
            if x[player, t].solution_value() > 0.5:
                match_lineup["players"].append(player)
                player_counts[player] += 1
                match_goals += G[players.index(player)]
        match_lineup["goals"] = match_goals
        match_lineups.append(match_lineup)
        total_goals += match_goals

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
