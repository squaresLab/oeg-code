from gurobi_stackelberg_equilibrium_solver_extended import get_stackelberg, get_attacker_br
from harsanyi_nash_equilibrium_solver_extended import get_solution, strategies_p1, strategies_p2, getMixedStrategyProfile

import time

print("timestep,equilibrium,11,12,21,22,we1,we2,e1,e2,payoff,uniform,time")

for x in range(100):
    t = x + 1

    nash_start_time = time.time()
    solution = get_solution(timesteps=t)
    nash_duration = time.time() - nash_start_time

    random_profile = getMixedStrategyProfile(timesteps=t)

    stackelberg_start_time = time.time()
    m = get_stackelberg(timesteps=t)
    stackelberg_duration = time.time() - stackelberg_start_time

    ans = [v.x for v in m.getVars()]
    ans.append(m.objVal)

    linen = str(t) + ",nash,"
    lines = str(t) + ",stackelberg,"

    strategies_p1 = 3**3 # attacker
    strategies_p2 = 3 * t # defender

    stackelberg_length = 3 * 3 + strategies_p2
    nash_length = strategies_p1 + strategies_p2

    for x in range(nash_length):
        # linen += str(solution[x]) + ","
        if x < strategies_p1: # if we are in attacker, copy attackers nash action for computing defenders loss if playing uniform random
            random_profile[x] = solution[x]
    linen += str(solution.payoff(1)) + ","

    # for x in range(stackelberg_length):
    #     # since we want attacker to go first, add an offset for the first 3*3 x values
    #     if 0 <= x < 3*3:
    #         lines += str(ans[x+strategies_p2]) + ","
    #     else:
    #         lines += str(ans[x-3*3]) + ","

    lines += str(ans[3*3 + strategies_p2]) + ","

    # dp = []
    #
    # uniform = 1.0 / strategies_p2
    #
    # for x in range(strategies_p2):
    #     dp.append(uniform)
    #
    # br_to_random = get_attacker_br(dp, timesteps=t, debug=False)
    # rand = [v.x for v in br_to_random.getVars()]
    # rand.append(br_to_random.objVal)
    #
    # linen += str(random_profile.payoff(1))
    # lines += str(rand[3+3 + strategies_p2])

    linen += str(nash_duration)
    lines += str(stackelberg_duration)

    print(linen)
    print(lines)


