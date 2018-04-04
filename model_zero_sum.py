class ModelZeroSum:

    def __init__(self):
        self.a1_observed_chance = 0.1
        self.a2_observed_chance = 0.9
        self.failed_eviction_penalty = 1

    def expected_time_in_system(self, a, d):
        if a == 1:
            if d == 1:
                return 1
            elif d == 2:
                return 1 + (1 - self.a1_observed_chance) * (1 + self.failed_eviction_penalty)
            elif d == 3:
                return 0
            elif d == 4:
                return 2 + self.failed_eviction_penalty
        elif a == 2:
            if d == 1:
                return 1 + (1 - self.a2_observed_chance) * (1 + self.failed_eviction_penalty)
            elif d == 2:
                return 1
            elif d == 3:
                return 2 + self.failed_eviction_penalty
            elif d == 4:
                return 0

    def adjusted_system_time(self, a, d, t):
        technique_fit = 1

        if a != t:
                technique_fit *= 0.5

        return self.expected_time_in_system(a, d) * technique_fit

    def payoff_attacker(self, a, d, t):

        return self.adjusted_system_time(a, d, t)

    def payoff_defender(self, a, d, t):

        return -self.payoff_attacker(a, d, t)
