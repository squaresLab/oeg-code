from gurobi_stackelberg_equilibrium_solver_extended import get_stackelberg, get_attacker_br
from harsanyi_nash_equilibrium_solver_extended import get_solution, strategies_p1, strategies_p2, getMixedStrategyProfile

print("t1_prior,equilibrium,11,12,21,22,we1,we2,e1,e2,payoff,uniform")

for x in range(101):
    t = x + 1
    solution = get_solution(timesteps=t)

    random_profile = getMixedStrategyProfile(timesteps=t)

    m = get_stackelberg(timesteps=t)
    ans = [v.x for v in m.getVars()]
    ans.append(m.objVal)

    linen = str(t) + ",nash,"
    lines = str(t) + ",stackelberg,"
    for x in range(strategies_p1 + strategies_p2):
        linen += str(solution[x]) + ","
        s = x
        if 0 <= s < 4:
            s += 4
            random_profile[x] = solution[x]
        elif 3 < s < 8:
            s -= 4
        lines += str(ans[s]) + ","

    linen += str(solution.payoff(1)) + ","
    lines += str(ans[strategies_p1 + strategies_p2]) + ","

    br_to_random = get_attacker_br([.25, .25, .25, .25], timesteps=t, debug=False)
    rand = [v.x for v in br_to_random.getVars()]
    rand.append(br_to_random.objVal)

    linen += str(random_profile.payoff(1))
    lines += str(rand[strategies_p1 + strategies_p2])

    print(linen)
    print(lines)


