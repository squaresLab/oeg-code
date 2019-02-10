from gurobipy import *

from extended_model_gen import ModelExtendedGen


def get_attacker_br(dp, timesteps=2, p_t1=0.33, p_t2=0.33, p_tn=0.33,debug=True,ttp1_obs=0.1,ttp2_obs=0.9):
    model = ModelExtendedGen(ttp1_obs,ttp2_obs,horizon=timesteps)

    try:

        num_attackers = 2
        num_ttps = 2

        strategies_p1 = num_ttps**num_attackers
        #strategies_p2 = timesteps*num_ttps
        strategies_p2 = ((timesteps**2 + timesteps)/2)*(num_attackers+1)#plus one for pass tactic

        nation_prior = p_t1
        criminal_prior = p_t2
        none_prior = p_tn

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
                obj += nation_prior * model.payoff_defender_single_defender_arg(a_index + 1, d, 1) * p[d] * a[
                    0, a_index]
                obj += criminal_prior * model.payoff_defender_single_defender_arg(a_index + 1, d, 2) * p[d] * a[
                    1, a_index]
            obj += none_prior * model.payoff_defender_single_defender_arg(1, d, 3) * p[d]

        obj *= -1

        m.setObjective(obj, GRB.MINIMIZE)

        # Add constraints
        # defenders ps sum to 1
        m.addConstr(p.sum() == 1)
        # each attacker chooses one pure strategy
        m.addConstrs(a.sum(i, '*') == 1 for i in range(num_attackers))
        # each attacker type best responds to the defenders choices
        # build payoff values for each attacker type and attacker choice
        coeff = {(t, action): p.prod(
            {d: model.payoff_attacker_single_defender_arg(action + 1, d, t + 1) for d in
             range(strategies_p2)})
                 for action in range(num_ttps) for t in range(num_attackers)}

        # for each possible action, check that the chosen action is >= (i.e., that the attacker best responds)
        m.addConstrs(a.prod(coeff, t, '*') >= coeff[(t, action)]
                     for action in range(num_ttps) for t in range(num_attackers))

        # constrain the defender to the specified strategy
        m.addConstrs(p[x] == dp[x] for x in range(strategies_p2))

        m.optimize()

        return m

    except GurobiError:
        print('Error reported')


def get_stackelberg(timesteps=2, t1_prior=0.33, t2_prior=0.33, tn_prior=0.33, debug=False, ttp1_obs=0.1, ttp2_obs=0.9):
    model = ModelExtendedGen(ttp1_obs, ttp2_obs, horizon=timesteps)

    try:

        num_attackers = 2
        num_ttps = 2

        strategies_p1 = num_ttps**num_attackers
        # strategies_p2 = timesteps*num_ttps
        strategies_p2 = ((timesteps ** 2 + timesteps) // 2) * (num_attackers+1) # plus one for pass tactic case

        nation_prior = t1_prior
        criminal_prior = t2_prior
        no_attacker_prior = tn_prior

        # Create a new model
        m = Model("mip1")

        m.setParam('OutputFlag', debug)

        # Create variables
        # defenders actions
        p = m.addVars(strategies_p2, vtype=GRB.CONTINUOUS)
        # attackers actions
        a = m.addVars(num_attackers, num_ttps, vtype=GRB.BINARY)

        # Set objective
        obj = LinExpr()

        for d in range(strategies_p2):
            for a_index in range(num_ttps):
                obj += nation_prior * model.payoff_defender_single_defender_arg(a_index+1, d, 1) * p[d] * a[0, a_index]
                # print("added "+str(nation_prior)+" * "+str(model.payoff_defender_single_defender_arg(a_index+1, d, 1))+" * "+str(p[d])+" * "+str(a[0, a_index]))
                obj += criminal_prior * model.payoff_defender_single_defender_arg(a_index+1, d, 2) * p[d] * a[1, a_index]
                # print("added " + str(criminal_prior) + " * " + str(model.payoff_defender_single_defender_arg(a_index + 1, d, 2)) + " * " + str(p[d]) + " * " + str(a[1, a_index]))
            obj += no_attacker_prior * model.payoff_defender_single_defender_arg(1, d, 3) * p[d]
            # print("added " + str(no_attacker_prior) + " * " + str(
            #     model.payoff_defender_single_defender_arg(a_index + 1, d, 3)) + " * " + str(p[d]))

        obj *= -1
        m.setObjective(obj, GRB.MINIMIZE)

        # Add constraints
        # defenders ps sum to 1
        m.addConstr(p.sum() == 1.0)
        # each attacker chooses one pure strategy
        m.addConstrs(a.sum(i, '*') == 1 for i in range(num_attackers))
        # each attacker type best responds to the defenders choices
        # build payoff values for each attacker type and attacker choice
        coeff = {(t, action): p.prod({d: model.payoff_attacker_single_defender_arg(action+1, d, t+1) for d in range(strategies_p2)})
                 for action in range(num_ttps) for t in range(num_attackers)}

        # for each possible action, check that the chosen action is >= (i.e., that the attacker best responds)
        m.addConstrs(a.prod(coeff, t, '*') >= coeff[(t, action)]
                     for action in range(num_ttps) for t in range(num_attackers))

        m.optimize()

        return m

    except GurobiError:
        print('Error reported')

def main():

# 0.04 + model.payoff_defender_single_defender_arg(1, x, 1) * 0.3072 + model.payoff_defender_single_defender_arg(1, x, 2) * 0.6528
    div = 1.0/9.0

    # m = get_stackelberg(t1_prior=0.2112, t2_prior=0.2288, tn_prior=0.56, debug=True)
    # m = get_attacker_br([div,div,div,div,div,div,div,div,div],p_t1=0.2112, p_t2=0.2288, p_tn=0.56, debug=True)


    # m = get_stackelberg(t1_prior=0.352, t2_prior=0.088, tn_prior=0.56, debug=True)
    m = get_attacker_br([div,div,div,div,div,div,div,div,div],p_t1=0.352, p_t2=0.088, p_tn=0.56, debug=True)

    for v in m.getVars():
        print(v.varName, v.x)

    print('Obj:', m.objVal)


if __name__ == '__main__':
    main()

