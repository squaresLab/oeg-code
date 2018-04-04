from model_zero_sum import ModelZeroSum


class ModelGenSum(ModelZeroSum):

    def defense_cost(self, a, d):
        if d == 3:
            return 2
        elif d == 4:
            return 1
        elif d == 1:
            if a == 1:
                return 2
            elif a == 2:
                return self.a2_observed_chance * 1 + (1 - self.a2_observed_chance) * 2
        elif d == 2:
            if a == 2:
                return 1
            elif a == 1:
                return self.a1_observed_chance * 2 + (1 - self.a2_observed_chance) * 1

    def payoff_defender(self, a, d, t):

        return -self.payoff_attacker(a, d, t)*t-0.5*self.defense_cost(a, d)
