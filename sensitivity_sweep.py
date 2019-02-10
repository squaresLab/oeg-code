from gurobi_stackelberg_equilibrium_solver_extended import get_stackelberg, get_attacker_br
from harsanyi_nash_equilibrium_solver_extended import get_solution, getMixedStrategyProfile

timesteps = 2

num_attackers = 2
num_ttps = 2

strategies_p1 = num_ttps ** num_attackers
strategies_p2 = ((timesteps ** 2 + timesteps) // 2) * (
            num_attackers + 1)  # num_attackers+1 is nessissary for handleing pass tactic case

print("na_prior,t1_prior,t2_prior,equilibrium,11,12,21,22,e1,e2,p,we1,we2,wp,ae1,ae2,ap,payoff,uniform")

sweep_step=50

for no_attacker in range(sweep_step+1):
    for p1 in range(sweep_step+1):

        t1 = p1/float(sweep_step)
        tn = no_attacker/float(sweep_step)

        t2 = 1-t1

        mod = 1-tn

        t1 *= mod
        t2 *= mod

        # nash solver
        solution = get_solution(p_t1=t1,p_t2=t2,p_na=tn,timesteps=2)
        # uniform random for NE
        random_profile = getMixedStrategyProfile(p_t1=t1,p_t2=t2,p_na=tn,timesteps=2)
        # SE solver
        m = get_stackelberg(timesteps=2, t1_prior=t1, t2_prior=t2, tn_prior=tn, debug=False)
        ans = [v.x for v in m.getVars()]
        ans.append(m.objVal)

        linen = str(tn)+","+str(t1) + "," + str(t2) + ",nash,"
        lines = str(tn)+","+str(t1) + "," + str(t2) + ",stackelberg,"

        for x in range(strategies_p1 + strategies_p2):
            linen += str(solution[0][x]) + ","
            s = x
            if 0 <= s < 4:
                s += 9
                random_profile[x] = solution[0][x]
            elif 3 < s < 13:
                s -= 4
            lines += str(ans[s]) + ","

        if(len(solution)>1):
            print("Warning more than one NE: "+str(len(solution)))

        linen += str(solution[0].payoff(1)*-1) + ","
        lines += str(ans[strategies_p1 + strategies_p2]) + ","
        # SE response to uninformed strategy
        div = 1.0/9.0
        br_to_random = get_attacker_br([div,div,div,div,div,div,div,div,div], timesteps=2, p_t1=t1, p_t2=t2, p_tn=tn, debug=False)
        rand = [v.x for v in br_to_random.getVars()]
        rand.append(br_to_random.objVal)

        # for x in br_to_random.getVars():
        #     print(x.x)

        linen += str(random_profile.payoff(1)*-1)
        lines += str(rand[strategies_p1 + strategies_p2])

        print(linen)
        print(lines)


