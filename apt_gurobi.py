from gurobipy import *

A1_EXPOSE_CHANCE = 0.1
A2_EXPOSE_CHANCE = 0.9

WRONG_PENALTY = 1


def expected_time_in_system(a, d):
    if a == 1:
        if d == 1:
            return 1
        elif d == 2:
            return 1 + (1 - A1_EXPOSE_CHANCE) * (1 + WRONG_PENALTY)
        elif d == 3:
            return 0
        elif d == 4:
            return 2 + WRONG_PENALTY
    elif a == 2:
        if d == 1:
            return 1 + (1 - A2_EXPOSE_CHANCE) * (1 + WRONG_PENALTY)
        elif d == 2:
            return 1
        elif d == 3:
            return 2 + WRONG_PENALTY
        elif d == 4:
            return 0


def payoff_attacker(a, d, t):
    techniqueFit = 1

    if (a != t):
        techniqueFit *= 0.5;

    return expected_time_in_system(a, d) * techniqueFit


def payoff_defender(a, d, t):
    return -payoff_attacker(a, d, t)

try:

    strategies_p1 = 2
    strategies_p2 = 4

    type = 1

    nation = [[payoff_attacker(a+1, d+1, type) for d in range(strategies_p2)] for a in range(strategies_p1)]

    type = 2

    criminal = [[payoff_attacker(a+1, d+1, type) for d in range(strategies_p2)] for a in range(strategies_p1)]

    nation_prior = 0.5
    criminal_prior = 0.5

    # Create a new model
    m = Model("mip1")

    # Create variables
    p = [4]
    p[0] = m.addVar(vtype=GRB.CONTINUOUS, name="a")
    p[1] = m.addVar(vtype=GRB.CONTINUOUS, name="b")
    p[2] = m.addVar(vtype=GRB.CONTINUOUS, name="c")
    p[3] = m.addVar(vtype=GRB.CONTINUOUS, name="d")

    # Set objective
    obj = LinExpr();

    obj += nation_prior * 

    m.setObjective(obj, GRB.MAXIMIZE)

    # Add constraint: x + 2 y + 3 z <= 4
    m.addConstr(x + 2 * y + 3 * z <= 4, "c0")

    # Add constraint: x + y >= 1
    m.addConstr(x + y >= 1, "c1")

    m.optimize()

    for v in m.getVars():
        print(v.varName, v.x)

    print('Obj:', m.objVal)

    print(g)

    # for a in range(strategies_p1):
    #     for d in range(strategies_p2):
    #         pa = payoff_attacker(a+1, d+1, 1)
    #         pd = payoff_defender(a+1, d+1, 1)
    #         g[a][d][0] = pa
    #         g[a][d][1] = pd

except GurobiError:
    print('Error reported')