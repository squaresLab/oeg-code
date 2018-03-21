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
    # defenders actions
    p = m.addVars(4, vtype=GRB.CONTINUOUS)
    a = m.addVars(2, 2, vtype=GRB.BINARY)

    # Set objective
    obj = LinExpr();

    for d in range(4):
        for a_index in range(2):
            obj += nation_prior * payoff_defender(a_index+1, d+1, 1) * p[d] * a[0, a_index]
            obj += criminal_prior * payoff_defender(a_index+1, d+1, 2) * p[d] * a[1, a_index]

    m.setObjective(obj, GRB.MAXIMIZE)

    # Add constraints
    # defenders ps sum to 1
    m.addConstr(p.sum() == 1)
    # each attacker chooses one pure strategy
    m.addConstrs(a.sum(i, '*') == 1 for i in range(2))
    # each attacker type best responds to the defenders choices
    # build payoff values for each attacker type and attacker choice
    coeff = {(t, action): p.prod({d: payoff_attacker(action+1, d+1, t+1) for d in range(4)}) for action in range(2) for t in range(2)}
    # alternative action for each attacker, bit flip
    alt = {(t, action): p.prod({d: payoff_attacker(1-action+1, d+1, t+1) for d in range(4)}) for action in range(2) for t in range(2)}
    # each attacker type best responds
    constraintslhs = [a.prod(coeff, t, '*') for t in range(2)]
    constraintsrhs = [a.prod(alt, t, '*') for t in range(2)]

    test = a.prod(coeff, 0, '*')

    m.addConstrs(a.prod(coeff, t, '*') >= a.prod(alt, t, '*') for t in range(2))

    m.optimize()

    for v in m.getVars():
        print(v.varName, v.x)

    print('Obj:', m.objVal)

    # for a in range(strategies_p1):
    #     for d in range(strategies_p2):
    #         pa = payoff_attacker(a+1, d+1, 1)
    #         pd = payoff_defender(a+1, d+1, 1)
    #         g[a][d][0] = pa
    #         g[a][d][1] = pd

except GurobiError:
    print('Error reported')