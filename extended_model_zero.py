class ModelExtended:

    def __init__(self, ttp1_obs=0.1, ttp2_obs=0.9, ttp3_obs=0.5):
        self.a_observed_chance = [ttp1_obs, ttp2_obs, ttp3_obs]
        self.failed_eviction_penalty = 1

    def expected_time_in_system(self, a, wait, blind_evict):

        # sum over each timestep
        timesteps = wait + 1

        expected_time = 0

        hidden_chance = 1 - self.a_observed_chance[a - 1]

        for t in range(timesteps):
            expected_time += hidden_chance ** t

        # chance that we reach the blind eviction
        blind_evict_reached = hidden_chance ** (timesteps + 1)

        if blind_evict != a:
            expected_time += blind_evict_reached * (1 + self.failed_eviction_penalty)

        return expected_time

    def adjusted_system_time(self, a, wait, blind_evict, t):
        technique_fit = 1

        if a != t:
                technique_fit *= 0.5

        return self.expected_time_in_system(a, wait, blind_evict) * technique_fit

    def payoff_attacker(self, a, wait, blind_evict, t):

        return self.adjusted_system_time(a, wait, blind_evict, t)

    def payoff_defender(self, a, wait, blind_evict, t):

        return -self.payoff_attacker(a, wait, blind_evict, t)
