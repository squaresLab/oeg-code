from gurobi_stackelberg_equilibrium_solver_extended import get_stackelberg, get_attacker_br
from harsanyi_nash_equilibrium_solver_extended import get_solution, getMixedStrategyProfile

timesteps = 2

num_attackers = 2
num_ttps = 2

strategies_p1 = num_ttps ** num_attackers
# strategies_p2 = timesteps*num_ttps
strategies_p2 = ((timesteps ** 2 + timesteps) / 2) * (num_attackers + 1)  # plus one for pass tactic

print("na_prior,t1_prior,t2_prior,equilibrium,decoys,11,12,21,22,e1,e2,p,we1,we2,wp,ae1,ae2,ap,payoff,uniform")

# decoy_cost = 0.0065
decoy_cost = 0.03

tn = 0.30

sweep_steps = 70

for x in range(sweep_steps+1):

    t1 = x/float(sweep_steps)
    t2 = 1 - t1

    mod = 1 - tn

    t1 *= mod
    t2 *= mod

    best_nash = get_solution(p_t1=t1, p_t2=t2, p_na=tn, timesteps=2), 0
    best_stack = get_stackelberg(timesteps=2, t1_prior=t1, t2_prior=t2, tn_prior=tn, debug=False), 0
    for o in range(18):
        ttp1_obs = (o * 5 + 10) / 100.0
        ttp2_obs = (o / 2.0 + 90) / 100.0

        solution = get_solution(p_t1=t1, p_t2=t2, p_na=tn,timesteps=2, ttp1_obs=ttp1_obs, ttp2_obs=ttp2_obs)
        if (len(solution)>1):
            print("Warning multipile NEs!")
        m = get_stackelberg(timesteps=2, t1_prior=t1, t2_prior=t2, tn_prior=tn, debug=False, ttp1_obs=ttp1_obs, ttp2_obs=ttp2_obs)

        if solution[0].payoff(1) - decoy_cost * o > best_nash[0][0].payoff(1) - decoy_cost * best_nash[1]:
            best_nash = solution, o
        if m.objVal + decoy_cost * o < best_stack[0].objVal + decoy_cost * best_stack[1]:
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

    random_profile = getMixedStrategyProfile(p_t1=t1, p_t2=t2, p_na=tn, timesteps=2, ttp1_obs=ttp1_obs, ttp2_obs=ttp2_obs)

    for x in range(strategies_p1 + strategies_p2):
        linen += str(solution[0][x]) + ","
        s = x
        if 0 <= s < 4:
            s += 9
            random_profile[x] = solution[0][x]
        elif 3 < s < 13:
            s -= 4
        lines += str(ans[s]) + ","

    linen += str(solution[0].payoff(1)*-1) + ","
    lines += str(ans[strategies_p1 + strategies_p2]) + ","

    o = best_stack[1]

    ttp1_obs = (o * 5 + 10) / 100.0
    ttp2_obs = (o / 2.0 + 90) / 100.0

    div = 1.0/9.0
    br_to_random = get_attacker_br([div,div,div,div,div,div,div,div,div], timesteps=2, p_t1=t1, p_t2=t2, p_tn=tn, debug=False, ttp1_obs=ttp1_obs, ttp2_obs=ttp2_obs)
    rand = [v.x for v in br_to_random.getVars()]
    rand.append(br_to_random.objVal)

    linen += str(random_profile.payoff(1)*-1)
    lines += str(rand[strategies_p1 + strategies_p2])

    print(linen)
    print(lines)
