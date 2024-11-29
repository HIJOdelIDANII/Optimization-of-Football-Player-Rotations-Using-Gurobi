from gurobipy import Model, GRB, quicksum
from flask import Flask

def Best3Attackers():
# Data
    players = range(6)  # 6 attackers
    matches = range(10)  # 10 matches
    G = [1.7, 1.49, 1.27, 1.06, 0.85, 0.64]  # Goals per game for each player
    S = [[0, 5, 3, 2, 1, 4],  # Synergy matrix (Sij values)
         [5, 0, 4, 3, 2, 1],
         [3, 4, 0, 5, 2, 3],
         [2, 3, 5, 0, 4, 1],
         [1, 2, 2, 4, 0, 3],
         [4, 1, 3, 1, 3, 0]]
    alpha = 0.5  # Weight for synergy in the objective
    C = [1.5, 1.0, 0.5, 1.5, 1.0, 0.5, 1.5, 1.0, 0.5, 1.5]  # Match complexity: 1.5 = Hard, 1.0 = Medium, 0.5 = Easy

    # Model
    m = Model("Football Rotation with Synergy and Match Complexity")
    m.setParam('OutputFlag', 0)

    # Variables
    x = m.addVars(players, matches, vtype=GRB.BINARY, name="x")  # Player selection
    y = m.addVars(players, players, matches, vtype=GRB.BINARY, name="y")  # Player pairs in a match

    # Constraints
    # Team size
    for t in matches:
        m.addConstr(quicksum(x[i, t] for i in players) == 3, name=f"TeamSize_Match{t}")

    # Synergy variables definition
    for t in matches:
        for i in players:
            for j in players:
                if i < j:  # Only consider pairs (i, j) where i < j to avoid duplicates
                    m.addConstr(y[i, j, t] <= x[i, t], name=f"Synergy_Def_1_{i}_{j}_Match{t}")
                    m.addConstr(y[i, j, t] <= x[j, t], name=f"Synergy_Def_2_{i}_{j}_Match{t}")
                    m.addConstr(y[i, j, t] >= x[i, t] + x[j, t] - 1, name=f"Synergy_Def_3_{i}_{j}_Match{t}")

    # Consecutive match constraint
    for i in players:
        for t in range(len(matches) - 2):
            m.addConstr(x[i, t] + x[i, t+1] + x[i, t+2] <= 2, name=f"Consecutive_Player{i}_Match{t}")

    # Stronger team for harder matches
    for t in matches:
        m.addConstr(quicksum(G[i] * x[i, t] for i in players) >= C[t] * 0.5, name=f"Min_Goals_Match{t}")

    # Rest key players for easier matches
    for t in matches:
        if C[t] == 0.5:  # Easy match
            m.addConstr(quicksum(x[i, t] for i in players if G[i] >= 1.5) <= 1, name=f"Rest_Strong_Match{t}")

    # Objective
    goal_part = quicksum(C[t] * G[i] * x[i, t] for i in players for t in matches)
    synergy_part = quicksum(C[t] * S[i][j] * y[i, j, t] for i in players for j in players if i < j for t in matches)
    m.setObjective(goal_part + alpha * synergy_part, GRB.MAXIMIZE)

    # Solve
    m.optimize()

    # Output results
    print("Match lineups:")
    player_counts = [0] * len(players)  # To track total appearances for each player

    for t in matches:
        print(f"Match {t + 1}: ", end="")
        for i in players:
            if x[i, t].x > 0.5:
                print(f"Player {i + 1} ", end="")
                player_counts[i] += 1
        print()

    # Display player statistics
    print("\nPlayer statistics:")
    for i in players:
        print(f"Player {i + 1}: Played {player_counts[i]} matches")
Best3Attackers()