from gurobi_stackelberg_equilibrium_solver import get_stackelberg, get_attacker_br
from harsanyi_nash_equilibrium_solver import get_solution, strategies_p1, strategies_p2, getMixedStrategyProfile

print("t1_prior,equilibrium,decoys,11,12,21,22,we1,we2,e1,e2,payoff,uniform")

decoy_cost = 0.0065

for x in range(21):
    t1 = x/20.0
    best_nash = get_solution(t1), 0
    best_stack = get_stackelberg(t1, False), 0
    for o in range(18):
        ttp1_obs = (o * 5 + 10) / 100.0
        ttp2_obs = (o / 2.0 + 90) / 100.0

        solution = get_solution(t1,ttp1_obs,ttp2_obs)

        m = get_stackelberg(t1, False,ttp1_obs,ttp2_obs)

        if solution.payoff(1) - decoy_cost * o > best_nash[0].payoff(1) - decoy_cost * best_nash[1]:
            best_nash = solution, o
        if m.objVal - decoy_cost * o > best_stack[0].objVal - decoy_cost * best_stack[1]:
            best_stack = m, o

    linen = str(t1) + ",nash,"
    lines = str(t1) + ",stackelberg,"

    solution = best_nash[0]
    m = best_stack[0]
    ans = [v.x for v in m.getVars()]
    ans.append(m.objVal)

    linen += str(best_nash[1]) + ","
    lines += str(best_stack[1]) + ","

    o = best_nash[1]

    ttp1_obs = (o * 5 + 10) / 100.0
    ttp2_obs = (o / 2.0 + 90) / 100.0

    random_profile = getMixedStrategyProfile(t1, ttp1_obs, ttp2_obs)

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

    o = best_stack[1]

    ttp1_obs = (o * 5 + 10) / 100.0
    ttp2_obs = (o / 2.0 + 90) / 100.0

    br_to_random = get_attacker_br(t1, False, [.25, .25, .25, .25], ttp1_obs, ttp2_obs)
    rand = [v.x for v in br_to_random.getVars()]
    rand.append(br_to_random.objVal)

    linen += str(random_profile.payoff(1))
    lines += str(rand[strategies_p1 + strategies_p2])

    print(linen)
    print(lines)


