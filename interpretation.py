import random
import time
import sys

from gurobi_stackelberg_equilibrium_solver_extended import get_stackelberg_from_model
from extended_model_gen import ModelExtendedGen
from harsanyi_nash_equilibrium_solver_extended import get_solution_from_model

# appropriatness given as a(attacker type, TTP)
# p is active measure change to q
# attacker notice defender's active measure
header = "q(TTP1),q(TTP2),a(11),a(12),a(21),a(22),a(n1),a(n2),p(1),p(2),p(3),1,2,3,d(1),d(2),d(3),c(E1),c(E2),c(P),c(A),t1,t2,na,equilibrium,num_eqs,11,12,21,22,e1,e2,p,we1,we2,wp,ae1,ae2,ap,payoff"

def rand_priors(n):
    slice_points = []
    for x in range(n-1):
        slice_points.append(random.random())

    slice_points.sort()

    priors = []
    for x in range(n):
        if x == 0:
            priors.append(slice_points[x])
        elif x < n-1:
            priors.append(slice_points[x] - slice_points[x-1])
        else:
            priors.append(1 - slice_points[x-1])

    return priors


def print_model(model):
    for x in model.a_observed_chance:
        sys.stdout.write(str(x)+",")
    for attacker_type in model.technique_appropriateness:
        for ttp_value in attacker_type:
            sys.stdout.write(str(ttp_value) + ",")
    for x in model.active_measure_obs_prime:
        sys.stdout.write(str(x) + ",")
    for x in model.active_measure_not_noticed:
        sys.stdout.write(str(x) + ",")
    for x in model.attacker_disruptiveness:
        sys.stdout.write(str(x) + ",")
    for x in model.a_evict_cost:
        sys.stdout.write(str(x) + ",")
    sys.stdout.write(str(model.active_measure_cost)+",")


def print_nash_sol(solution, model, priors, strategies_p1, strategies_p2, num_eqs):
    print_model(model)
    sys.stdout.write(str(priors[0]) + "," + str(priors[1]) + "," + str(priors[2]) + ",nash,"+str(num_eqs)+",")
    linen = ""
    for x in range(strategies_p1 + strategies_p2):
        linen += str(solution[x]) + ","

    linen += str(solution.payoff(1) * -1)
    sys.stdout.write(linen)
    sys.stdout.write("\n")


def main(args):
    # assumption, limit to 2 timesteps, 2 attackers and 2 ttps, with no attacker case and pass tactic available
    timesteps = 2
    num_attackers = 2
    num_ttps = 2

    random.seed(568468+int(args[2]))

    trials = 10000

    #print(header)

    start = time.time()

    for x in range(trials):
        ttp1_obs = random.random()
        ttp2_obs = random.random()

        model = ModelExtendedGen(ttp1_obs, ttp2_obs, horizon=timesteps)
        # all ttps have 0 appropriateness for the no attacker case
        appropriateness = [[random.random() if y < num_attackers else 0 for x in range(num_ttps)] for y in range(num_attackers+1)]
        model.technique_appropriateness = appropriateness

        model.active_measure_obs_prime = [random.uniform(0, ttp1_obs), random.uniform(0, ttp2_obs), 0]  # trailing 0 since no attacker is not observable

        model.active_measure_not_noticed = [random.random() for x in range(num_ttps)]
        model.active_measure_not_noticed.append(1)  # append 1 since no attacker cant notice

        # assumption, disruptivness can be between 0, 10
        model.attacker_disruptiveness = [random.uniform(0, 10) for x in range(num_attackers)]
        model.attacker_disruptiveness.append(0)  # append 0 since no attacker type is not disruptive

        # assumption cost can be at most timesteps * max disruptiveness
        max_disrupt = max(model.attacker_disruptiveness)
        model.a_evict_cost = [random.uniform(0, timesteps*max_disrupt) for x in range(num_ttps)]
        model.a_evict_cost.append(0)  # append 0 since pass tactic has no cost

        model.active_measure_cost = random.uniform(0, timesteps*max_disrupt)

        priors = rand_priors(num_attackers+1)

        go_nash = go_stackelberg = True

        if len(args) > 1:
            if args[1] == "nash":
                go_stackelberg = False
            elif args[1] == "stackelberg":
                go_nash = False
            else:
                print("Invalid Arg")
                sys.exit()

        strategies_p1 = num_ttps ** num_attackers
        # strategies_p2 = timesteps*num_ttps
        strategies_p2 = ((timesteps ** 2 + timesteps) // 2) * (num_attackers + 1)  # plus one for pass tactic case

        if go_nash:
            nash_solution = get_solution_from_model(model, p_t1=priors[0], p_t2=priors[1], p_na=priors[2])

            for solution in nash_solution:
                print_nash_sol(solution, model, priors, strategies_p1, strategies_p2, len(nash_solution))

        if go_stackelberg:
            stackelberg_solution = get_stackelberg_from_model(model, t1_prior=priors[0], t2_prior=priors[1], tn_prior=priors[2])
            print_model(model)
            sys.stdout.write(str(priors[0])+","+str(priors[1])+","+str(priors[2])+",stackelberg,1,")
            ans = [v.x for v in stackelberg_solution.getVars()]
            ans.append(stackelberg_solution.objVal)
            lines = ""
            for s in range(strategies_p1 + strategies_p2):
                if 0 <= s < 4:
                    s += 9
                elif 3 < s < 13:
                    s -= 4
                lines += str(ans[s]) + ","
            lines += str(ans[strategies_p1 + strategies_p2])
            sys.stdout.write(lines)
            sys.stdout.write("\n")

    # print (time.time() - start)


if __name__ == "__main__":
    main(sys.argv)
