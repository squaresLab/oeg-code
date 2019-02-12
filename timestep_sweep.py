from gurobi_stackelberg_equilibrium_solver_extended import get_stackelberg, get_attacker_br
from harsanyi_nash_equilibrium_solver_extended import get_solution, getMixedStrategyProfile

import time

timesteps = 2

num_attackers = 2
num_ttps = 2

print("timesteps,equilibrium,payoff,time")

max_timesteps = 100
trials = 5


for x in range(max_timesteps):
    t = x + 1
    for trial in range(trials):

        timesteps = t

        strategies_p1 = num_ttps ** num_attackers
        strategies_p2 = ((timesteps ** 2 + timesteps) // 2) * (
                num_attackers + 1)  # num_attackers+1 is nessissary for handleing pass tactic case

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

        stackelberg_length = strategies_p1 + strategies_p2
        nash_length = strategies_p1 + strategies_p2

        for x in range(nash_length):
            # linen += str(solution[x]) + ","
            if x < strategies_p1: # if we are in attacker, copy attackers nash action for computing defenders loss if playing uniform random
                random_profile[x] = solution[0][x]
        linen += str(solution[0].payoff(1)) + ","

        # for x in range(stackelberg_length):
        #     # since we want attacker to go first, add an offset for the first 3*3 x values
        #     if 0 <= x < 3*3:
        #         lines += str(ans[x+strategies_p2]) + ","
        #     else:
        #         lines += str(ans[x-3*3]) + ","

        lines += str(ans[strategies_p1 + strategies_p2]) + ","

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


