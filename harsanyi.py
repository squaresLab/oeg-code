import gambit
from math import ceil
from decimal import *

from model_zero_sum import ModelZeroSum

strategies_p1 = 4
strategies_p2 = 4

g = gambit.Game.new_table([strategies_p1, strategies_p2])

g.title = "APT Observability"

g.players[0].label = "Attacker"
g.players[1].label = "Defender"

T1_PRIOR = 0.1
T2_PRIOR = 0.9

model = ModelZeroSum()

a = 0
for a1 in range(2):
    for a2 in range(2):
        for d in range(strategies_p2):
            pa = T1_PRIOR * model.payoff_attacker(a1+1, d+1, 1) + T2_PRIOR * model.payoff_attacker(a2+1, d+1, 2)
            pd = T1_PRIOR * model.payoff_defender(a1+1, d+1, 1) + T2_PRIOR * model.payoff_defender(a2+1, d+1, 2)
            g[a, d][0] = Decimal(pa)
            g[a, d][1] = Decimal(pd)
        a += 1

g
s = gambit.nash.ExternalEnumMixedSolver()


print(s.solve(g))