import gambit
from math import ceil
from decimal import *

from extended_model_gen import ModelExtendedGen


def get_solution_from_model(model, p_t1=0.33, p_t2=0.33, p_na=0.33, num_attackers=2, num_ttps=2):
    timesteps = model.horizon
    strategies_p1 = num_ttps ** num_attackers
    strategies_p2 = ((timesteps ** 2 + timesteps) // 2) * (num_attackers + 1)  # num_attackers+1 is nessissary for handleing pass tactic case

    g = gambit.Game.new_table([strategies_p1, strategies_p2])

    g.title = "APT Observability"

    g.players[0].label = "Attacker"
    g.players[1].label = "Defender"

    a = 0
    for a1 in range(2):
        for a2 in range(2):
            for d in range(strategies_p2):
                pa = p_t1 * model.payoff_attacker_single_defender_arg(a1 + 1, d,
                                                                          1) + p_t2 * model.payoff_attacker_single_defender_arg(
                    a2 + 1, d, 2) + p_na * model.payoff_attacker_single_defender_arg(a2 + 1, d, 3)
                pd = p_t1 * model.payoff_defender_single_defender_arg(a1 + 1, d,
                                                                          1) + p_t2 * model.payoff_defender_single_defender_arg(
                    a2 + 1, d, 2) + p_na * model.payoff_defender_single_defender_arg(a2 + 1, d, 3)
                # print(str(pa) + " " + str(pd))
                g[a, d][0] = Decimal(pa)
                g[a, d][1] = Decimal(pd)
            a += 1

    s = gambit.nash.ExternalEnumMixedSolver()

    solution = s.solve(g)
    return solution

def get_solution(timesteps=2, p_t1=0.33, p_t2=0.33, p_na=0.33, ttp1_obs=0.1, ttp2_obs=0.9):

    strategies_p2 = 3 * timesteps

    t1_prior = p_t1
    t2_prior = p_t2
    t3_prior = p_na

    num_attackers = 2
    num_ttps = 2

    strategies_p1 = num_ttps ** num_attackers
    # strategies_p2 = timesteps*num_ttps
    strategies_p2 = ((timesteps ** 2 + timesteps) // 2) * (num_attackers+1) # num_attackers+1 is nessissary for handleing pass tactic case

    nation_prior = t1_prior
    criminal_prior = t2_prior
    no_attacker_prior = t3_prior

    g = gambit.Game.new_table([strategies_p1, strategies_p2])

    g.title = "APT Observability"

    g.players[0].label = "Attacker"
    g.players[1].label = "Defender"

    model = ModelExtendedGen(ttp1_obs, ttp2_obs, horizon=timesteps)

    a = 0
    for a1 in range(2):
        for a2 in range(2):
            for d in range(strategies_p2):
                pa = t1_prior * model.payoff_attacker_single_defender_arg(a1+1, d, 1) + t2_prior * model.payoff_attacker_single_defender_arg(a2+1, d, 2) + t3_prior * model.payoff_attacker_single_defender_arg(a2+1, d, 3)
                pd = t1_prior * model.payoff_defender_single_defender_arg(a1+1, d, 1) + t2_prior * model.payoff_defender_single_defender_arg(a2+1, d, 2) + t3_prior * model.payoff_defender_single_defender_arg(a2+1, d, 3)
                # print(str(pa) + " " + str(pd))
                g[a, d][0] = Decimal(pa)
                g[a, d][1] = Decimal(pd)
            a += 1

    s = gambit.nash.ExternalEnumMixedSolver()

    solution = s.solve(g)
    return solution


def getMixedStrategyProfile(timesteps=2, p_t1=0.33, p_t2=0.33, p_na=0.33, ttp1_obs=0.1, ttp2_obs=0.9):
    t1_prior = p_t1
    t2_prior = p_t2
    t3_prior = p_na

    num_attackers = 2
    num_ttps = 2

    strategies_p1 = num_ttps ** num_attackers
    strategies_p2 = ((timesteps ** 2 + timesteps) // 2) * (num_attackers+1) # num_attackers+1 is nessissary for handleing pass tactic case

    g = gambit.Game.new_table([strategies_p1, strategies_p2])

    g.title = "APT Observability"

    g.players[0].label = "Attacker"
    g.players[1].label = "Defender"

    model = ModelExtendedGen(ttp1_obs, ttp2_obs)

    a = 0
    for a1 in range(2):
        for a2 in range(2):
                for d in range(strategies_p2):
                    pa = t1_prior * model.payoff_attacker_single_defender_arg(a1 + 1, d, 1) + t2_prior * model.payoff_attacker_single_defender_arg(a2 + 1, d, 2) + t3_prior * model.payoff_attacker_single_defender_arg(a2 + 1, d, 3)
                    pd = t1_prior * model.payoff_defender_single_defender_arg(a1 + 1, d, 1) + t2_prior * model.payoff_defender_single_defender_arg(a2 + 1, d, 2) + t3_prior * model.payoff_defender_single_defender_arg(a2 + 1, d, 3)
                    g[a, d][0] = Decimal(pa)
                    g[a, d][1] = Decimal(pd)
                a += 1

    s = gambit.nash.ExternalEnumMixedSolver()

    return g.mixed_strategy_profile()



def main():
    timesteps=50
    num_attackers = 2
    num_ttps = 2

    strategies_p1 = num_ttps ** num_attackers
    # strategies_p2 = timesteps*num_ttps
    strategies_p2 = ((timesteps ** 2 + timesteps) // 2) * (num_attackers + 1)  # plus one for pass tactic case

    solution = get_solution(timesteps=timesteps, p_t1=0.33, p_t2=0.33, p_na=0.33)

    if (len(solution)==1):
        solution = solution[0]
    else:
        print("Warning multiple NE's!")

    print(solution)
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
