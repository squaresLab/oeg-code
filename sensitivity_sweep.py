from harsanyi_nash_equilibrium_solver import get_solution, strategies_p1, strategies_p2

print("t1_prior,11,12,21,22,we1,we2,e1,e2,payoff")

for x in range(101):
    t1 = x/100.0
    solution = get_solution(t1)

    line = str(t1) + ","
    for x in range(strategies_p1 + strategies_p2):
        line += str(solution[x]) + ","

    line += str(solution.payoff(1))

    print(line)
