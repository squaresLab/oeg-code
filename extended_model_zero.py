class ModelExtended(object):

    def __init__(self, ttp1_obs=0.1, ttp2_obs=0.9, ttp3_obs=0.5, horizon=3):
        self.a_observed_chance = [ttp1_obs, ttp2_obs, ttp3_obs]
        self.failed_eviction_timesteps = horizon
        self.evict_chance = 0
        self.active_measure_failed = 0

    @staticmethod
    def active_measure_modifier(hidden_chance, a):
        if a == 1:
            return 0.85
        elif a == 2:
            return 0.05
        elif a == 3:
            return 0.45
        else:
            return -1

    @staticmethod
    def active_measure_missed(a):
        if a == 1:
            return 0.1
        elif a == 2:
            return 0.9
        elif a == 3:
            return 0.5
        else:
            return -1

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
                    expected_time += reach_chance * self.failed_eviction_timesteps
            else:
                # if not an eviction tactic
                if t == active_measure:
                    # if we are during the active measure
                    # chance that the attacker notices and defender fails
                    self.active_measure_failed = reach_chance * (1 - self.active_measure_missed(a))
                    expected_time += self.active_measure_failed * self.failed_eviction_timesteps
                    # chance that attacker does not notice, and we get better at noticing
                    hidden_chance = self.active_measure_modifier(hidden_chance, a)
                    reach_chance *= self.active_measure_missed(a)
                    # defender has a chance to notice the attacker now

                # if there is no active measure, or there is but we havent reached it yet
                # consider that we may identify and evict the attacker
                expected_time += reach_chance * t * (1-hidden_chance)
                # consider that we may continue
                reach_chance *= hidden_chance

        self.evict_chance = reach_chance
        return expected_time

    def adjusted_system_time(self, a, wait, blind_evict, t, active_measure=-1):
        technique_fit = 1

        if a != t:
                technique_fit *= 0.5

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
