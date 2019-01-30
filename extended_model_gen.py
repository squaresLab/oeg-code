from extended_model_zero import ModelExtended
import math


class ModelExtendedGen(ModelExtended):

    def __init__(self, *args, **kwargs):
        super(ModelExtendedGen, self).__init__(*args, **kwargs)
        self.a_evict_cost = [1, 0.5, 0.75]
        self.active_measure_cost = .5
        self.no_attacker_type = 4

    @staticmethod
    def triangular_root(n):
        return (math.sqrt((8 * n) + 1) - 1) / 2

    def defense_cost(self, a, wait, blind_evict, active_measure=-1):
        cost = 0

        # if not exposed and not active measure failed, pay blind eviction cost
        cost += self.evict_chance * self.a_evict_cost[blind_evict - 1]

        # if exposed, pay attackers a evict cost
        exposed_chance = 1 - self.evict_chance - self.active_measure_failed
        cost += exposed_chance * self.a_evict_cost[a - 1]

        # if active measure used, pay its use cost
        if active_measure >= 0:
            if self.active_measure_failed == 0 and self.evict_chance == 1:
                cost += self.active_measure_cost
            else:
                cost += (self.active_measure_failed / (1-self.active_measure_missed(a))) * self.active_measure_cost

        return cost

    def payoff_defender(self, a, wait, blind_evict, t, active_measure=-1):

        if t == self.no_attacker_type:
            self.active_measure_failed = 0
            self.evict_chance = 1
            return -self.defense_cost(a, wait, blind_evict, active_measure)
        else:
            return -self.payoff_attacker(a, wait, blind_evict, t, active_measure)*t-self.defense_cost(a, wait, blind_evict, active_measure)

    def payoff_defender_single_defender_arg(self, a, d, t):
        # how many timesteps? the triangular root of d
        num_ttps = 3
        trig = (d // num_ttps) + 1
        root = self.triangular_root(trig)
        prev_root = self.triangular_root(trig-1)
        timesteps = math.ceil(root)
        floor = math.floor(prev_root)
        start = ((floor**2 + floor)/2) + 1
        active_place = trig - start - 1

        if active_place < 0:
            active_place = -1
            wait = timesteps - 1
        else:
            wait = timesteps - 2

        blind_evict = d % num_ttps + 1

        return self.payoff_defender(a, wait, blind_evict, t, active_place)


def main():
    model = ModelExtendedGen()
    ans = model.payoff_defender(3, 0, 3, 3)
    print(ans)


if __name__ == "__main__":
    main()
