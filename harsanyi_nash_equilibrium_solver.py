import gambit
from math import ceil
from decimal import *

from model_zero_sum import ModelZeroSum

strategies_p1 = 4
strategies_p2 = 4


def get_solution(p_t1):

    t1_prior = p_t1
    t2_prior = 1 - p_t1

    g = gambit.Game.new_table([strategies_p1, strategies_p2])

    g.title = "APT Observability"

    g.players[0].label = "Attacker"
    g.players[1].label = "Defender"

    model = ModelZeroSum()

    a = 0
    for a1 in range(2):
        for a2 in range(2):
            for d in range(strategies_p2):
                pa = t1_prior * model.payoff_attacker(a1+1, d+1, 1) + t2_prior * model.payoff_attacker(a2+1, d+1, 2)
                pd = t1_prior * model.payoff_defender(a1+1, d+1, 1) + t2_prior * model.payoff_defender(a2+1, d+1, 2)
                g[a, d][0] = Decimal(pa)
                g[a, d][1] = Decimal(pd)
            a += 1

    s = gambit.nash.ExternalEnumMixedSolver()

    solution = s.solve(g)[0]
    return solution


def main():

    solution = get_solution(0.1)

    line = ""
    for x in range(strategies_p1 + strategies_p2):
        line += str(solution[x])
        if x < strategies_p1 + strategies_p2 - 1:
            line += ","

    print(line)
    print(solution)


if __name__ == "__main__":
    main()
