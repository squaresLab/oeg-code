import gambit
from decimal import Decimal

tau = 2
# must_attack_by = tau + 1  # where 0 indicates first timestep and tau indicates does not attack
num_ttps = 2
ttp_obs = (Decimal('.1'), Decimal('0.9'))
priors = [Decimal('0.5'), Decimal('0.5')]
num_attacker_types = len(priors)

# defender eviction actions, chance to evict each TTP
defender_eviction_actions = [((1, 0), 1),
                             ((0, 1), Decimal('0.5')),
                             ((0, 0), 0)]
# defender observation actions, change to obs, chance to get noticed, cost
defender_observation_actions = [((1, 1), (0, 0), 0),
                                ((Decimal('.95'), Decimal('.95')), (Decimal('.9'), Decimal('.1')), Decimal('.1'))]

# cost of defenders actions, eviction first, then obs
action_cost = (1, Decimal('.5'), 0, 0, Decimal('.1'))

# appropriateness to type of TTP
appropriateness = [(1, Decimal('.5')),
                   (Decimal('.5'), 1)]

# disruptiveness of type to the defender
disruptiveness = [1, 2]


def check_type(val):
    if isinstance(val, gambit.lib.libgambit.Decimal) or isinstance(val, Decimal):
        return val
    else:
        return gambit.Decimal.from_float(val)


def payoff_attacker(time_step, attacker_type, attacker_ttp):
    return check_type(time_step * appropriateness[attacker_type][attacker_ttp])


def payoff_defender(time_step, attacker_type, attacker_ttp, defenders_cost):
    return check_type(
        -payoff_attacker(time_step, attacker_type, attacker_ttp) * disruptiveness[attacker_type] - defenders_cost)


def payoff_attacker_failed_eviction(time_step, attacker_type, attacker_ttp):
    return check_type(payoff_attacker(tau, attacker_type, attacker_ttp))


def payoff_defender_failed_eviction(time_step, attacker_type, attacker_ttp, defenders_cost):
    return check_type(-payoff_attacker_failed_eviction(tau, attacker_type, attacker_ttp) * disruptiveness[
        attacker_type] - defenders_cost)


defender_actions = len(defender_eviction_actions) + len(defender_observation_actions)

g = gambit.Game.new_tree()

g.title = "Observable Eviction Game"

defender = g.players.add("Defender")
attacker = g.players.add("Attacker")
chance = g.players.chance
chance.label = "Nature"

root = g.root


def fill_defender_observational_node(cur_node, time_step, attacker_type, attacker_ttp, ttp_obs, defenders_cost, infoset_index):
    # now have a chance to detect the attacker
    not_noticed_move = cur_node.append_move(chance, 2)
    not_noticed_move.label = "Defender Observes Attacker"
    not_observed_node = cur_node.children[0]
    not_observed_node.prior_action.prob = 1 - ttp_obs[attacker_ttp]

    # if not observed, game continues
    infoset_index = fill_defender_actions(cur_node.children[0], time_step + 1, attacker_type, attacker_ttp, ttp_obs, defenders_cost, infoset_index)

    # if observed, game ends w/ payoff values
    observed_outcome = g.outcomes.add("Attacker observed and evicted")
    observed_outcome[0] = payoff_defender(time_step, attacker_type, attacker_ttp,
                                          defenders_cost + action_cost[attacker_ttp])
    observed_outcome[1] = payoff_attacker(time_step, attacker_type, attacker_ttp)
    observed_node = cur_node.children[1]
    observed_node.outcome = observed_outcome
    observed_node.prior_action.prob = ttp_obs[attacker_ttp]

    return infoset_index


def fill_defender_actions(cur_node, time_step, attacker_type, attacker_ttp, ttp_obs, defenders_cost, infoset_index):
    # if tau timesteps have been reached, then the defender may only perform eviction actions
    defender_action_limit = 0

    if time_step == tau - 1:
        defender_action_limit = len(defender_observation_actions)

    if infoset_index == len(defender.infosets):
        m = cur_node.append_move(defender, defender_actions - defender_action_limit)
        m.label = "Defender Moves at timestep " + str(time_step)
    else:
        m = cur_node.append_move(defender.infosets[infoset_index])

    infoset_index += 1

    parent_node = cur_node
    # for each defender action, generate chance nodes where appropriate
    for defender_move in range(defender_actions - defender_action_limit):
        # get the current move node
        cur_node = parent_node.children[defender_move]
        # check if this action if obs or eviction
        if defender_move >= len(defender_eviction_actions):
            # this is an observation action
            obs_index = defender_move - len(defender_eviction_actions)

            # if not noticed, modify observability
            change = defender_observation_actions[obs_index][0]
            q_prime = ()
            for i in change:
                q_prime = q_prime + (1 - change[len(q_prime)] * (1 - ttp_obs[len(q_prime)]),)

            # check if this observation action has a chance to be noticed
            if defender_observation_actions[obs_index][1][attacker_ttp] > 0:
                # this obs action may be noticed, generate a chance node that the attacker notices
                notice_move = cur_node.append_move(chance, 2)
                notice_move.label = "Attacker notices defender's active measure"

                # fill in tree for not noticed
                not_noticed_node = cur_node.children[0]

                not_noticed_node.prior_action.prob = 1 - defender_observation_actions[obs_index][1][attacker_ttp]
                infoset_index = fill_defender_observational_node(not_noticed_node, time_step, attacker_type, attacker_ttp, q_prime,
                                                                 defenders_cost + action_cost[defender_move], infoset_index)

                # if noticed, game ends w/ payoff values
                noticed_node = cur_node.children[1]
                noticed_node.prior_action.prob = defender_observation_actions[obs_index][1][attacker_ttp]
                noticed_outcome = g.outcomes.add("Attacker noticed defender's action")
                noticed_outcome[0] = payoff_defender_failed_eviction(time_step, attacker_type, attacker_ttp,
                                                                     defenders_cost + action_cost[defender_move])
                noticed_outcome[1] = payoff_attacker_failed_eviction(time_step, attacker_type, attacker_ttp)
                noticed_node.outcome = noticed_outcome

            else:  # this observation action has no chance to be noticed by the attacker, just fill defender's obs part
                infoset_index = fill_defender_observational_node(cur_node, time_step, attacker_type, attacker_ttp, q_prime,
                                                                 defenders_cost + action_cost[defender_move], infoset_index)
        else:  # this actions is an eviction action
            # get eviction success / fail payoff values
            eviction_fail_outcome = g.outcomes.add("Failed Eviction")
            eviction_fail_value = payoff_defender_failed_eviction(time_step, attacker_type, attacker_ttp,
                                                                  defenders_cost + action_cost[defender_move])
            eviction_fail_outcome[0] = eviction_fail_value
            eviction_fail_outcome[1] = payoff_attacker_failed_eviction(time_step, attacker_type, attacker_ttp)

            eviction_succeeds_outcome = g.outcomes.add("Successful Eviction")
            eviction_succeeds_outcome[0] = payoff_defender(time_step, attacker_type, attacker_ttp,
                                                           defenders_cost + action_cost[defender_move])
            eviction_succeeds_outcome[1] = payoff_attacker(time_step, attacker_type, attacker_ttp)

            # check if this eviction is probabilistic
            eviction_chance = defender_eviction_actions[defender_move][0][attacker_ttp]
            if eviction_chance == 0 or eviction_chance == 1:
                # game ends directly
                if eviction_chance == 0:
                    cur_node.outcome = eviction_fail_outcome
                    eviction_succeeds_outcome.delete()
                else:
                    cur_node.outcome = eviction_succeeds_outcome
                    eviction_fail_outcome.delete()
            else:
                # game ends probabilistically
                eviction_move = cur_node.append_move(chance, 2)
                eviction_move.label = "Eviction attempt"

                # if eviction fails
                eviction_fail_node = cur_node.children[0]
                eviction_fail_node.prior_action.prob = gambit.Decimal.from_float(1 - eviction_chance)
                eviction_fail_node.outcome = eviction_fail_outcome

                # if eviction succeeds
                eviction_succeeds_node = cur_node.children[1]
                eviction_succeeds_node.prior_action.prob = gambit.Decimal.from_float(eviction_chance)
                eviction_succeeds_node.outcome = eviction_succeeds_outcome
    return infoset_index


# first nature chooses which attacker type defender plays against
m = root.append_move(chance, num_attacker_types)
m.label = "Nature chooses attacker type"

#defender_choice_node = root.children[attacker_type].children[attacker_ttp]
for attacker_type_index in range(num_attacker_types):
    attacker_type_node = root.children[attacker_type_index]
    # the attacker now gets to choose a TTP
    m = attacker_type_node.append_move(attacker, num_ttps)
    m.label = "Attacker type "+str(attacker_type_index)+" chooses TTP"
    for attacker_ttp_index in range(num_ttps):
        attacker_ttp_node = attacker_type_node.children[attacker_ttp_index]
        # fill in the rest of the tree for the defender
        fill_defender_actions(attacker_ttp_node, 0, attacker_type_index, attacker_ttp_index, ttp_obs, 0, 0)

print(g.write())
# # now nature chooses what timestep the attacker starts attacking
# first_node = root.children[0]
# m = first_node.append_move(chance, must_attack_by)
# m.label = "Nature chooses attack start time"
# # must be done for each branch of attacker type
# cur_node = first_node.next_sibling
# while cur_node is not None:
#     # note that nature's choices are all within same info set at each level of tree
#     # does this matter? I don't think so
#     cur_node.append_move(m)
#     cur_node = cur_node.next_sibling
