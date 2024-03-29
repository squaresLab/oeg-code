from gurobipy import *

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


def get_stackelberg(t1_prior, debug, ttp1_obs=0.1, ttp2_obs=0.9):

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
                obj += nation_prior * model.payoff_defender(a_index+1, d+1, 1) * p[d] * a[0, a_index]
                obj += criminal_prior * model.payoff_defender(a_index+1, d+1, 2) * p[d] * a[1, a_index]

        m.setObjective(obj, GRB.MAXIMIZE)

        # Add constraints
        # defenders ps sum to 1
        m.addConstr(p.sum() == 1)
        # each attacker chooses one pure strategy
        m.addConstrs(a.sum(i, '*') == 1 for i in range(2))
        # each attacker type best responds to the defenders choices
        # build payoff values for each attacker type and attacker choice
        coeff = {(t, action): p.prod({d: model.payoff_attacker(action+1, d+1, t+1) for d in range(4)})
                 for action in range(2) for t in range(2)}
        # alternative action for each attacker, bit flip
        alt = {(t, action): p.prod({d: model.payoff_attacker(1-action+1, d+1, t+1) for d in range(4)})
               for action in range(2) for t in range(2)}

        # each attacker type best responds
        m.addConstrs(a.prod(coeff, t, '*') >= a.prod(alt, t, '*') for t in range(2))

        m.optimize()

        return m

    except GurobiError:
        print('Error reported')

def main():

    m = get_stackelberg(0.1, True)

    for v in m.getVars():
        print(v.varName, v.x)

    print('Obj:', m.objVal)


if __name__ == '__main__':
    main()

