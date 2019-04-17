class ModelExtended(object):

    def __init__(self, ttp1_obs=0.1, ttp2_obs=0.9, horizon=2):
        # internal calculations only
        self.evict_chance = 0
        self.active_measure_failed = 0

        # model parameters
        self.a_observed_chance = [ttp1_obs, ttp2_obs]
        self.horizon = horizon
        self.active_measure_not_noticed = [0.1, 0.9, 0.5]  # not noticed by the attacker
        self.active_measure_obs_prime = [0.855, 0.095, 0.45]
        self.technique_appropriateness = [[1, 0.5],
                                          [0.5, 1]]

    def technique_fit(self, t, a):
        return self.technique_appropriateness[t-1][a-1]

    def active_measure_modifier(self, hidden_chance, a):
        return self.active_measure_obs_prime[a-1]

# active measure is missed by the attacker, i.e., the chance that that measure succeeds
    def active_measure_missed(self, a):
        return self.active_measure_not_noticed[a-1]

    # failed eviction penalty paramteterized by time and attacker TTP
    def failed_eviction_timesteps(self, t, a):
        penalty = 0
        # if a == 2:
        #     penalty = t/self.horizon * 1.0

        return self.horizon + penalty

    def expected_time_in_system(self, a, wait, blind_evict, active_measure=-1):

        # sum over each timestep
        timesteps = wait + 1
        if active_measure >= 0:
            timesteps += 1

        expected_time = 0

        reach_chance = 1

        hidden_chance = 1 - self.a_observed_chance[a - 1]

        self.active_measure_failed = 0

        for t in range(timesteps):
            # if an eviction tactic
            if t == timesteps - 1:
                if blind_evict != a:
                    expected_time += reach_chance * self.failed_eviction_timesteps(t,a)
                else:
                    expected_time += reach_chance * t
            else:
                # if not an eviction tactic
                if t == active_measure:
                    # if we are during the active measure
                    # chance that the attacker notices and defender fails
                    self.active_measure_failed = reach_chance * (1 - self.active_measure_missed(a))
                    expected_time += self.active_measure_failed * self.failed_eviction_timesteps(t,a)
                    # chance that attacker does not notice, and we get better at noticing
                    hidden_chance = self.active_measure_modifier(hidden_chance, a)
                    reach_chance *= self.active_measure_missed(a)
                    # defender has a chance to notice the attacker now

                # if there is no active measure, or there is but we havent reached it yet
                # consider that we may identify and evict the attacker
                # TODO also, consider that we may choose not to evict the attacker if we lose more utility by doing so
                #remain_chance = hidden_chance
                # if util_from_evict < util_from_pass
                # remain_chance = 1
                expected_time += reach_chance * t * (1-hidden_chance)
                # consider that we may continue
                reach_chance *= hidden_chance

        self.evict_chance = reach_chance
        return expected_time

    def adjusted_system_time(self, a, wait, blind_evict, t, active_measure=-1):
        technique_fit = self.technique_fit(t, a)
        # technique_fit = 1
        #
        # # if a != t:
        # #         technique_fit *= 0.5

        return self.expected_time_in_system(a, wait, blind_evict, active_measure) * technique_fit

    def payoff_attacker(self, a, wait, blind_evict, t, active_measure=-1):

        return self.adjusted_system_time(a, wait, blind_evict, t, active_measure)

    def payoff_defender(self, a, wait, blind_evict, t, active_measure=-1):

        return -self.payoff_attacker(a, wait, blind_evict, t, active_measure)

def main():
    model = ModelExtended()
    ans = model.expected_time_in_system(1, 2, 2, 1)
    print(ans)


if __name__ == "__main__":
    main()
