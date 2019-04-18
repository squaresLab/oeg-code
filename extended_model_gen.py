from extended_model_zero import ModelExtended
import math


class ModelExtendedGen(ModelExtended):

    def __init__(self, *args, **kwargs):
        super(ModelExtendedGen, self).__init__(*args, **kwargs)
        self.a_evict_cost = [1, 0.5, 0]
        self.active_measure_cost = .1
        self.no_attacker_type = 3
        self.attacker_disruptiveness = [1, 2]

    @staticmethod
    def triangular_root(n):
        return (math.sqrt((8 * n) + 1) - 1) / 2

    def disruptiveness(self, t):
        return self.attacker_disruptiveness[t-1]

    # old defense cost function before conditional evict on waits
    def defense_cost(self, a, wait, blind_evict, active_measure=-1):
        cost = 0

        # if not exposed and not active measure failed, pay blind eviction cost
        cost += self.evict_chance * self.a_evict_cost[blind_evict - 1]

        # if exposed, pay attackers a evict cost
        # TODO unless the cost to evict is higher than the cost to allow to remain
        exposed_chance = 1 - self.evict_chance - self.active_measure_failed
        cost += exposed_chance * self.a_evict_cost[a - 1]

        # if active measure used, pay its use cost
        if active_measure >= 0:
            if self.active_measure_failed == 0 and self.evict_chance == 1:
                cost += self.active_measure_cost
            else:
                cost += (self.active_measure_failed / (1-self.active_measure_missed(a))) * self.active_measure_cost

        return cost

    # def defense_cost(self, a, wait, blind_evict, t, active_measure=-1):
    #     # sum over each timestep
    #     timesteps = wait + 1
    #     if active_measure >= 0:
    #         timesteps += 1
    #
    #     expected_cost = 0
    #
    #     reach_chance = 1
    #
    #     hidden_chance = 1 - self.a_observed_chance[a - 1]
    #
    #     self.active_measure_failed = 0
    #
    #     for t in range(timesteps):
    #         # if an eviction tactic
    #         if t == timesteps - 1:
    #             expected_cost += self.a_evict_cost[blind_evict-1]
    #         else:
    #             # if not an eviction tactic
    #             if t == active_measure:
    #                 # if we are during the active measure
    #                 # chance that the attacker notices and defender fails
    #                 self.active_measure_failed = reach_chance * (1 - self.active_measure_missed(a))
    #                 expected_cost += self.active_measure_cost
    #                 # chance that attacker does not notice, and we get better at noticing
    #                 hidden_chance = self.active_measure_modifier(hidden_chance, a)
    #                 reach_chance *= self.active_measure_missed(a)
    #                 # defender has a chance to notice the attacker now
    #
    #             # if there is no active measure, or there is but we havent reached it yet
    #             # consider that we may identify and evict the attacker
    #             # if util_from_evict < util_from_pass
    #             time_left = self.horizon - t
    #             attacker_util_remain = time_left * self.technique_fit(t, a)
    #             defender_util_remain = attacker_util_remain * self.disruptiveness(t) # no cost since we just wait
    #             cost_to_evict = self.a_evict_cost[a-1]
    #
    #             if cost_to_evict > defender_util_remain:
    #                 pass
    #             else:
    #                 expected_cost += self.a_evict_cost[a-1] * (1-hidden_chance) * reach_chance
    #             # consider that we may continue
    #             reach_chance *= hidden_chance
    #
    #     self.evict_chance = reach_chance
    #     return expected_cost

    # def expected_time_in_system(self, a, wait, blind_evict, t, active_measure=-1):
    #     # sum over each timestep
    #     timesteps = wait + 1
    #     if active_measure >= 0:
    #         timesteps += 1
    #
    #     expected_time = 0
    #
    #     reach_chance = 1
    #
    #     hidden_chance = 1 - self.a_observed_chance[a - 1]
    #
    #     self.active_measure_failed = 0
    #
    #     for t in range(timesteps):
    #         # if an eviction tactic
    #         if t == timesteps - 1:
    #             if blind_evict != a:
    #                 expected_time += reach_chance * self.failed_eviction_timesteps(t, a)
    #             else:
    #                 expected_time += reach_chance * t
    #         else:
    #             # if not an eviction tactic
    #             if t == active_measure:
    #                 # if we are during the active measure
    #                 # chance that the attacker notices and defender fails
    #                 self.active_measure_failed = reach_chance * (1 - self.active_measure_missed(a))
    #                 expected_time += self.active_measure_failed * self.failed_eviction_timesteps(t, a)
    #                 # chance that attacker does not notice, and we get better at noticing
    #                 hidden_chance = self.active_measure_modifier(hidden_chance, a)
    #                 reach_chance *= self.active_measure_missed(a)
    #                 # defender has a chance to notice the attacker now
    #
    #             # if there is no active measure, or there is but we havent reached it yet
    #             # consider that we may identify and evict the attacker
    #             # if util_from_evict < util_from_pass
    #             time_left = self.horizon - t
    #             attacker_util_remain = time_left * self.technique_fit(t, a)
    #             defender_util_remain = attacker_util_remain * self.disruptiveness(t) # no cost since we just wait
    #             cost_to_evict = self.a_evict_cost[a-1]
    #
    #             if cost_to_evict > defender_util_remain:
    #                 # if too expensive to evict, we choose to pass and let them stay till the end
    #                 expected_time += reach_chance * self.horizon * (1 - hidden_chance)
    #             else:
    #                 expected_time += reach_chance * t * (1 - hidden_chance)
    #             # consider that we may continue
    #             reach_chance *= hidden_chance
    #
    #     self.evict_chance = reach_chance
    #     return expected_time

    def payoff_defender(self, a, wait, blind_evict, t, active_measure=-1):

        if t == self.no_attacker_type:
            self.active_measure_failed = 0
            self.evict_chance = 1  # that is, the chance of reaching the evict tactic
            return -self.defense_cost(a, wait, blind_evict, active_measure)
        else:
            return -self.payoff_attacker(a, wait, blind_evict, t, active_measure)*self.disruptiveness(t)-self.defense_cost(a, wait, blind_evict, active_measure)

    def payoff_attacker_single_defender_arg(self, a, d, t):
        # how many timesteps? the triangular root of d
        num_ttps = 2+1  # also need to add 1 for the pass tactic
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

        wait = int(wait)

        return self.payoff_attacker(a, wait, blind_evict, t, active_place)

    def payoff_defender_single_defender_arg(self, a, d, t):
        # how many timesteps? the triangular root of d
        num_ttps = 2+1  # also need to add 1 for the pass tactic
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

        wait = int(wait)

        blind_evict = d % num_ttps + 1

        return self.payoff_defender(a, wait, blind_evict, t, active_place)


def main():
    model = ModelExtendedGen()
    # sum = 0
    # for x in range(9):
    #     sum += model.payoff_defender_single_defender_arg(1, x, 3) * 0.56 + model.payoff_defender_single_defender_arg(1, x, 1) * 0.352 + model.payoff_defender_single_defender_arg(1, x, 2) * 0.088
    # print(str(sum/9.0))

    # sum = 0
    # x=0
    # sum += model.payoff_defender_single_defender_arg(2, x, 3) * 0.04 + model.payoff_defender_single_defender_arg(2, x, 1) * 0.3072 + model.payoff_defender_single_defender_arg(2, x, 2) * 0.6528
    # print(str(sum))

    # sum = 0
    # for x in range(9):
    #     sum += model.payoff_attacker_single_defender_arg(1, x, 2)
    # print(str(sum/9.0))

    print("ttp1 def: "+str(model.payoff_defender_single_defender_arg(1, 3, 1)))
    print("ttp1 attacker: "+str(model.payoff_attacker_single_defender_arg(1, 3, 1)))
    print("ttp2 def: "+str(model.payoff_defender_single_defender_arg(2, 3, 1)))
    print("ttp2 attacker: "+str(model.payoff_attacker_single_defender_arg(2, 3, 1)))

if __name__ == "__main__":
    main()
