import gambit

tau = 2
must_attack_by = tau + 1 # where 0 indicates first timestep and tau indicates does not attack
num_ttps = 2
priors = [0.5, 0.5]
num_attacker_types = len(priors)

defender_eviction_actions = num_ttps
defender_observation_actions = 2
defender_actions = defender_eviction_actions + defender_observation_actions

g = gambit.Game.new_tree() #type: gambit.Game

g.title = "Observable Eviction Game"

defender = g.players.add("Defender")
attacker = g.players.add("Attacker")
chance = g.players.chance
chance.label = "Nature"

root = g.root

# first nature chooses which attacker type defender plays against
m = root.append_move(chance, num_attacker_types)
m.label = "Nature chooses attacker type"

# now nature chooses what timestep the attacker starts attacking
first_node = root.children[0]
m = first_node.append_move(chance, must_attack_by)
m.label = "Nature chooses attack start time"
# must be done for each branch of attacker type
cur_node = first_node.next_sibling
while cur_node is not None:
    # note that nature's choices are all within same info set at each level of tree
    # does this matter? I don't think so
    cur_node.append_move(m)
    cur_node = cur_node.next_sibling

# the attacker chooses a TTP
cur_node = root.children[0].children[0]
m = cur_node.append_move(attacker, num_ttps)
m.label = "Attacker chooses TTP"
# must be done for each branch
cur_node = cur_node.next_sibling
while cur_node is not None:
    # note that that each attacker choice in its own info set, indicating that the attacker
    # knows their own type and when they attack... maybe should not know about when?
    m = cur_node.append_move(attacker, num_ttps)
    m.label = "Attacker chooses TTP"
    cur_node = cur_node.next_sibling

# start the defender's portion of the game tree
first_node = root.children[0].children[0]
for timestep in range(tau):
    first_node = first_node.children[0]
    # for each timestep, the defender needs to choose between their actions
    m = first_node.append_move(defender, defender_actions)
    m.label = "Defender chooses an action for time "+str(timestep)
    # needs to occur at all branches
    cur_node = first_node.next_sibling
    while cur_node is not None:
        cur_node.append_move(m)
        cur_node = cur_node.next_sibling
