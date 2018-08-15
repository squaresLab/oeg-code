from gurobipy import *

from extended_model_gen import ModelExtendedGen
from model_gen_sum import ModelGenSum


def get_attacker_br(t1_prior,debug,dp,ttp1_obs=0.1,ttp2_obs=0.9):
    model = ModelGenSum(ttp1_obs,ttp2_obs)

    try:

        strategies_p1 = 2
        strategies_p2 = 4

        nation_prior = t1_prior
        criminal_prior = 1 - t1_prior

        # Create a new model
        m = Model("mip1")

        m.setParam('OutputFlag', debug)

        # Create variables
        # defenders actions
        p = m.addVars(4, vtype=GRB.CONTINUOUS)
        a = m.addVars(2, 2, vtype=GRB.BINARY)

        # Set objective
        obj = LinExpr()

        for d in range(4):
            for a_index in range(2):
                obj += nation_prior * model.payoff_defender(a_index + 1, d + 1, 1) * p[d] * a[0, a_index]
                obj += criminal_prior * model.payoff_defender(a_index + 1, d + 1, 2) * p[d] * a[1, a_index]

        m.setObjective(obj, GRB.MAXIMIZE)

        # Add constraints
        # defenders ps sum to 1
        m.addConstr(p.sum() == 1)
        # each attacker chooses one pure strategy
        m.addConstrs(a.sum(i, '*') == 1 for i in range(2))
        # each attacker type best responds to the defenders choices
        # build payoff values for each attacker type and attacker choice
        coeff = {(t, action): p.prod({d: model.payoff_attacker(action + 1, d + 1, t + 1) for d in range(4)})
                 for action in range(2) for t in range(2)}
        # alternative action for each attacker, bit flip
        alt = {(t, action): p.prod({d: model.payoff_attacker(1 - action + 1, d + 1, t + 1) for d in range(4)})
               for action in range(2) for t in range(2)}

        # each attacker type best responds
        m.addConstrs(a.prod(coeff, t, '*') >= a.prod(alt, t, '*') for t in range(2))

        # constrain the defender to the specified strategy
        m.addConstrs(p[x] == dp[x] for x in range(4))

        m.optimize()

        return m

    except GurobiError:
        print('Error reported')


def get_stackelberg(t1_prior=0.33, t2_prior=0.33, t3_prior=0.33, debug=False, ttp1_obs=0.1, ttp2_obs=0.9, ttp3_obs=0.5):

    model = ModelExtendedGen(ttp1_obs, ttp2_obs, ttp3_obs)

    try:

        num_attackers = 3
        timesteps = 3
        num_ttps = 3

        strategies_p1 = num_ttps**num_attackers
        strategies_p2 = timesteps*num_ttps

        nation_prior = t1_prior
        criminal_prior = t2_prior
        terrorist_prior = t3_prior

        # Create a new model
        m = Model("mip1")

        m.setParam('OutputFlag', debug)

        # Create variables
        # defenders actions
        p = m.addVars(strategies_p2, vtype=GRB.CONTINUOUS)
        a = m.addVars(num_attackers, num_ttps, vtype=GRB.BINARY)

        # Set objective
        obj = LinExpr()

        for d in range(strategies_p2):
            for a_index in range(num_ttps):
                obj += nation_prior * model.payoff_defender_single_defender_arg(a_index+1, d, 1) * p[d] * a[0, a_index]
                obj += criminal_prior * model.payoff_defender_single_defender_arg(a_index+1, d, 2) * p[d] * a[1, a_index]
                obj += terrorist_prior * model.payoff_defender_single_defender_arg(a_index+1, d, 3) * p[d] * a[2, a_index]

        m.setObjective(obj, GRB.MAXIMIZE)

        # Add constraints
        # defenders ps sum to 1
        m.addConstr(p.sum() == 1)
        # each attacker chooses one pure strategy
        m.addConstrs(a.sum(i, '*') == 1 for i in range(num_attackers))
        # each attacker type best responds to the defenders choices
        # build payoff values for each attacker type and attacker choice
        coeff = {(t, action): p.prod({d: model.payoff_attacker(action+1, d/num_ttps, (d % num_ttps)+1, t+1) for d in range(strategies_p2)})
                 for action in range(num_ttps) for t in range(num_attackers)}

        # for each possible action, check that the chosen action is >= (i.e., that the attacker best responds)
        m.addConstrs(a.prod(coeff, t, '*') >= coeff[(t, action)]
                     for action in range(num_ttps) for t in range(num_attackers))

        m.optimize()

        return m

    except GurobiError:
        print('Error reported')

def main():

    m = get_stackelberg(debug=True)

    for v in m.getVars():
        print(v.varName, v.x)

    print('Obj:', m.objVal)


if __name__ == '__main__':
    main()

