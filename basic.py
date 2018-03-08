import gambit
from math import ceil
from decimal import *

MAX_NOISE = 10.0

strategies_p1 = 10
strategies_p2 = 10

g = gambit.Game.new_table([strategies_p1, strategies_p2])

g.title = "APT Observability"

g.players[0].label = "Attacker"
g.players[1].label = "Defender"

EXPLORATION_NOISE = 1
EXPLOITATION_NOISE = 1


def expected_time_in_system(a, d):
    survived_exploration = 1
    if a >= d:
        # must roll for caught during exploration
        survived_exploration = 1 - ((a*EXPLORATION_NOISE) / MAX_NOISE)
        # after this, expected time is based on the exploitation rate
        chance_caught_each_cycle = a / MAX_NOISE
        expected_cycles = 1 / chance_caught_each_cycle

        if expected_cycles*survived_exploration == 0:
            print("?")

        return expected_cycles*survived_exploration

    else:
        time_till_first_roll = ceil(-((a*EXPLORATION_NOISE) - d)/EXPLOITATION_NOISE)
        survived_first_roll = 1 - (a*EXPLORATION_NOISE + time_till_first_roll * EXPLOITATION_NOISE) / MAX_NOISE

        chance_caught_each_cycle = d / MAX_NOISE
        expected_cycles = 1 / chance_caught_each_cycle
        time_per_cycle = d / (a * EXPLOITATION_NOISE)

        return time_till_first_roll * (1-survived_first_roll) + survived_first_roll * (time_per_cycle * expected_cycles + time_till_first_roll)


def payoff_attacker(a, d):
    return expected_time_in_system(a,d)*a*a


def payoff_defender(a, d):
    return -expected_time_in_system(a,d)*a


for a in range(strategies_p1):
    for d in range(strategies_p2):
        pa = payoff_attacker(a+1, d+1)
        pd = payoff_defender(a+1, d+1)
        g[a, d][0] = Decimal(pa)
        g[a, d][1] = Decimal(pd)

g
s = gambit.nash.ExternalEnumMixedSolver()

qre = gambit.qre.ExternalStrategicQREPathTracer()

print(s.solve(g))