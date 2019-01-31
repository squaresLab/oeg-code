import gambit
from math import ceil
from decimal import *

from extended_model_gen import ModelExtendedGen

strategies_p1 = 3**3
strategies_p2 = 3*3


def get_solution(timesteps=3, p_t1=0.25, p_t2=0.25, p_t3=0.25, p_t4=0.25, ttp1_obs=0.1, ttp2_obs=0.9, ttp3_obs=0.5):

    strategies_p2 = 3 * timesteps

    t1_prior = p_t1
    t2_prior = p_t2
    t3_prior = p_t3
    t4_prior = p_t4

    num_attackers = 3
    num_ttps = 3

    strategies_p1 = num_ttps ** num_attackers
    # strategies_p2 = timesteps*num_ttps
    strategies_p2 = ((timesteps ** 2 + timesteps) // 2) * num_attackers

    nation_prior = t1_prior
    criminal_prior = t2_prior
    terrorist_prior = t3_prior
    no_attacker_prior = t4_prior

    g = gambit.Game.new_table([strategies_p1, strategies_p2])

    g.title = "APT Observability"

    g.players[0].label = "Attacker"
    g.players[1].label = "Defender"

    model = ModelExtendedGen(ttp1_obs, ttp2_obs, ttp3_obs, horizon=timesteps)

    a = 0
    for a1 in range(3):
        for a2 in range(3):
            for a3 in range(3):
                for d in range(strategies_p2):
                    pa = t1_prior * model.payoff_attacker_single_defender_arg(a1+1, d, 1) + t2_prior * model.payoff_attacker_single_defender_arg(a2+1, d, 2) + t3_prior * model.payoff_attacker_single_defender_arg(a3+1, d, 3) + t4_prior * model.payoff_attacker_single_defender_arg(a3+1, d, 4)
                    pd = t1_prior * model.payoff_defender_single_defender_arg(a1+1, d, 1) + t2_prior * model.payoff_defender_single_defender_arg(a2+1, d, 2) + t3_prior * model.payoff_defender_single_defender_arg(a3+1, d, 3) + t4_prior * model.payoff_defender_single_defender_arg(a3+1, d, 4)
                    g[a, d][0] = Decimal(pa)
                    g[a, d][1] = Decimal(pd)
                a += 1

    s = gambit.nash.ExternalEnumMixedSolver()

    solution = s.solve(g)[0]
    return solution


def getMixedStrategyProfile(timesteps=3, p_t1=0.33, p_t2=0.33, p_t3=0.33, ttp1_obs=0.1, ttp2_obs=0.9, ttp3_obs=0.5):
    t1_prior = p_t1
    t2_prior = p_t2
    t3_prior = p_t3

    strategies_p2 = 3 * timesteps

    g = gambit.Game.new_table([strategies_p1, strategies_p2])

    g.title = "APT Observability"

    g.players[0].label = "Attacker"
    g.players[1].label = "Defender"

    model = ModelExtendedGen(ttp1_obs, ttp2_obs, ttp3_obs)

    a = 0
    for a1 in range(3):
        for a2 in range(3):
            for a3 in range(3):
                for wait in range(timesteps):
                    for blind in range(3):
                        pa = t1_prior * model.payoff_attacker(a1 + 1, wait, blind + 1, 1) + t2_prior * model.payoff_attacker(a2 + 1, wait, blind + 1, 2) + t3_prior * model.payoff_attacker(a3 + 1, wait, blind + 1, 3)
                        pd = t1_prior * model.payoff_defender(a1 + 1, wait, blind + 1,1) + t2_prior * model.payoff_defender(a2 + 1, wait, blind + 1, 2) + t3_prior * model.payoff_defender(a3 + 1, wait, blind + 1, 3)
                        g[a, wait * 3 + blind][0] = Decimal(pa)
                        g[a, wait * 3 + blind][1] = Decimal(pd)
                a += 1

    s = gambit.nash.ExternalEnumMixedSolver()

    return g.mixed_strategy_profile()



def main():

    solution = get_solution()

    line = ""
    for x in range(strategies_p1 + strategies_p2):
        line += str(solution[x])
        if x < strategies_p1 + strategies_p2 - 1:
            line += ","

    print(line)
    print(solution)
    print(solution.payoff(1))


if __name__ == "__main__":
    main()
