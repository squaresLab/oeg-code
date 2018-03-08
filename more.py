import gambit
from math import ceil
from decimal import *

# MAX_NOISE = 10.0

strategies_p1 = 2
strategies_p2 = 4

g = gambit.Game.new_table([strategies_p1, strategies_p2])

g.title = "APT Observability"

g.players[0].label = "Attacker"
g.players[1].label = "Defender"

A1_EXPOSE_CHANCE = 0.1
A2_EXPOSE_CHANCE = 0.9

WRONG_PENALTY = 1


def expected_time_in_system(a, d):
    if a == 1:
        if d == 1:
            return 1
        elif d == 2:
            return 1 + (1-A1_EXPOSE_CHANCE) * (1 + WRONG_PENALTY)
        elif d == 3:
            return 0
        elif d == 4:
            return 2 + WRONG_PENALTY
    elif a == 2:
        if d == 1:
            return 1 + (1-A2_EXPOSE_CHANCE) * (1 + WRONG_PENALTY)
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

    return expected_time_in_system(a,d) * techniqueFit


def payoff_defender(a, d, t):
    return -payoff_attacker(a,d,t)


for a in range(strategies_p1):
    for d in range(strategies_p2):
        pa = payoff_attacker(a+1, d+1, 1)
        pd = payoff_defender(a+1, d+1, 1)
        g[a, d][0] = Decimal(pa)
        g[a, d][1] = Decimal(pd)

g
s = gambit.nash.ExternalEnumMixedSolver()


print(s.solve(g))