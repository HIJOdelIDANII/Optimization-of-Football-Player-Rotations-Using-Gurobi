from gurobipy import Model, GRB, quicksum

def Best3Attackers():
    players = range(6)  # 6 attackers
    matches = range(38)  # 38 matches
    G = [1.5, 1.6, 1.27, 1.06, 0.5, 0.2]  # Goals per game for each player
    P = [3, 2, 2, 1, 1, 1]  # Maximum consecutive matches based on physicality
    C = [1.0, 0.5, 1.5, 1.0, 0.5, 1.5, 1.0, 0.5, 1.5, 1.0, 0.5, 1.5,
         1.0, 0.5, 1.5, 1.0, 0.5, 1.5, 1.0, 0.5, 1.5, 1.0, 0.5, 1.5,
         1.0, 0.5, 1.5, 1.0, 0.5, 1.5, 1.0, 0.5, 1.5, 1.0, 0.5, 1.5,
         1.0, 0.5]

    m = Model("Football Rotation with Synergy and Match Complexity")
    m.setParam('OutputFlag', 0)

    x = m.addVars(players, matches, vtype=GRB.BINARY, name="x")  # Player selection

    # Team size
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
            m.addConstr(quicksum(x[i, t] for i in players if G[i] <= 0.7) >= 2, name=f"Rest_Strong_Match{t}")

    # Objective
    goal_part = quicksum(C[t] * G[i] * x[i, t] for i in players for t in matches)
    m.setObjective(goal_part, GRB.MAXIMIZE)

    m.optimize()

    # Check if the model is solved
    if m.status != GRB.OPTIMAL:
        print("Optimization failed!")
        return

    print("Match lineups:")
    player_counts = [0] * len(players)  # To track total appearances for each player
    total_goals = 0  # To calculate total goals for the season

    for t in matches:
        print(f"Match {t + 1}: ", end="")
        match_goals = 0  # Goals for this match
        for i in players:
            if x[i, t].X > 0.5:  # Use .X to access variable values
                print(f"Player {i + 1} ", end="")
                player_counts[i] += 1
                match_goals += G[i]  # Add the player's goals to the match total
        print(f" | Goals scored: {match_goals:.2f}")
        total_goals += match_goals  # Add match goals to season total

    # Display player statistics
    print("\nPlayer statistics:")
    for i in players:
        print(f"Player {i + 1}: Played {player_counts[i]} matches")

    print(f"\nTotal goals scored in the season: {total_goals:.2f}")

Best3Attackers()
