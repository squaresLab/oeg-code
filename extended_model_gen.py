from extended_model_zero import ModelExtended


class ModelExtendedGen(ModelExtended):

    def __init__(self, *args, **kwargs):
        super(ModelExtendedGen, self).__init__(*args, **kwargs)
        self.a_evict_cost = [2, 1, 1.5]

    def defense_cost(self, a, wait, blind_evict):
        # chance exposed
        timesteps = wait + 1

        chance_hidden = 1 - self.a_observed_chance[a-1]

        chance_hidden = (chance_hidden ** timesteps)

        chance_exposed = 1 - chance_hidden

        cost = 0

        # if exposed, pay attackers a evict cost
        cost += chance_exposed * self.a_evict_cost[a - 1]
        # if not exposed, pay blind eviction cost
        cost += chance_hidden * self.a_evict_cost[blind_evict - 1]

        return cost

    def payoff_defender(self, a, wait, blind_evict, t):

        return -self.payoff_attacker(a, wait, blind_evict, t)*t-0.5*self.defense_cost(a, wait, blind_evict)

    def payoff_defender_single_defender_arg(self, a, d, t):
        num_ttps = 3
        wait = d / num_ttps
        blind_evict = d % num_ttps + 1
        return self.payoff_defender(a, wait, blind_evict, t)
