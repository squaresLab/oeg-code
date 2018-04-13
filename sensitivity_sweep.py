from gurobi_stackelberg_equilibrium_solver import get_stackelberg, get_attacker_br
from harsanyi_nash_equilibrium_solver import get_solution, strategies_p1, strategies_p2, getMixedStrategyProfile

print("t1_prior,equilibrium,11,12,21,22,we1,we2,e1,e2,payoff,uniform")

for x in range(101):
    t1 = x/100.0
    solution = get_solution(t1)

    random_profile = getMixedStrategyProfile(t1)

    m = get_stackelberg(t1, False)
    ans = [v.x for v in m.getVars()]
    ans.append(m.objVal)

    linen = str(t1) + ",nash,"
    lines = str(t1) + ",stackelberg,"
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

    br_to_random = get_attacker_br(t1, False, [.25, .25, .25, .25])
    rand = [v.x for v in br_to_random.getVars()]
    rand.append(br_to_random.objVal)

    linen += str(random_profile.payoff(1))
    lines += str(rand[strategies_p1 + strategies_p2])

    print(linen)
    print(lines)


