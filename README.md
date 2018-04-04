#APT Observability
## Game Theory Code

Important Files:
+`model_zero_sum.py` This file provides methods to obtain the payoff values for the defender.
This includes necessary helper tasks like computing the attacker's expected time in the system.
Zero-sum means that the attacker and defenders payoffs are the opposite of one another.
+'model_gen_sum.py' This file extends the zero-sum version of the model to a general-sum case.
There is an extra method for computing the defenders cost to evict each attacker TTP.
Additionally, the defender suffers an extra penalty for allowing TTP2 to remain in the system.
+`harsanyi_nash_equilibrium_solver` This file uses the Harsanyi transform to solve the Nash equilibrium.
It requires that the Gambit library for python be installed. See http://www.gambit-project.org/gambit13/pyapi.html
+`gurobi_stackelberg_equilibrium_solver` This file uses mathematical programming to solve for the Stackelberg equilibrium.
It requires that the Gurobi optimiser be installed, see http://www.gurobi.com/resources/seminars-and-videos/modeling-with-the-gurobi-python-interface
