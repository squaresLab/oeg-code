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

def adjusted_system_time(a, d, t):
    techniqueFit = 1

    if a != t:
        if t == 1:
            techniqueFit *= 0.5
        elif t == 2:
            techniqueFit *= 0.5

    return expected_time_in_system(a, d) * techniqueFit


def payoff_attacker(a, d, t):

    return adjusted_system_time(a,d,t)


def defense_cost(a,d):
    if d == 3:
        return 2
    elif d == 4:
        return 1
    elif d == 1:
        if a == 1:
            return 2
        elif a == 2:
            return A2_EXPOSE_CHANCE * 1 + (1-A2_EXPOSE_CHANCE)*2
    elif d == 2:
        if a == 2:
            return 1
        elif a ==1:
            return A1_EXPOSE_CHANCE * 2 + (1-A2_EXPOSE_CHANCE)*1


def payoff_defender(a, d, t):

    return -payoff_attacker(a,d,t)*t-0.5*defense_cost(a,d)

type = 1

for a in range(strategies_p1):
    for d in range(strategies_p2):
        pa = payoff_attacker(a+1, d+1, type)
        pd = payoff_defender(a+1, d+1, type)
        g[a, d][0] = Decimal(pa)
        g[a, d][1] = Decimal(pd)

s = gambit.nash.ExternalEnumMixedSolver()


print(s.solve(g))

strategies_p1 = 4
strategies_p2 = 4

g = gambit.Game.new_table([strategies_p1, strategies_p2])

T1_PRIOR = 0.5
T2_PRIOR = 0.5

a = 0
for a1 in range(2):
    for a2 in range(2):
        for d in range(strategies_p2):
            pa = T1_PRIOR * payoff_attacker(a1+1, d+1, 1) + T2_PRIOR * payoff_attacker(a2+1, d+1, 2)
            pd = T1_PRIOR * payoff_defender(a1+1, d+1, 1) + T2_PRIOR * payoff_defender(a2+1, d+1, 2)
            g[a, d][0] = Decimal(pa)
            g[a, d][1] = Decimal(pd)
        a += 1

g
s = gambit.nash.ExternalEnumMixedSolver()

print(s.solve(g))