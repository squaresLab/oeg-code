import csv
import math


def triangular_root(n):
    return (math.sqrt((8 * n) + 1) - 1) / 2

def parse_defender_actions(d):
    # how many timesteps? the triangular root of d
    num_ttps = 2+1  # also need to add 1 for the pass tactic
    trig = (d // num_ttps) + 1
    root = triangular_root(trig)
    prev_root = triangular_root(trig-1)
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

    return wait, blind_evict, active_place

header = "timesteps,q(TTP1),q(TTP2),a(11),a(12),a(21),a(22),a(n1),a(n2),p(1),p(2),p(3),1,2,3,d(1),d(2),d(3),c(E1),c(E2),c(P),c(A),t1,t2,na,equilibrium,num_eqs,11,12,21,22,e1,e2,p,we1,we2,wp,ae1,ae2,ap,payoff"
post_proc_header = "timesteps,q(TTP1),q(TTP2),a(11),a(12),a(21),a(22),a(n1),a(n2),p(1),p(2),p(3),1,2,3,d(1),d(2),d(3),c(E1),c(E2),c(P),c(A),t1,t2,na,equilibrium,num_eqs,11,12,21,22,wait,active,pass,payoff"

print(post_proc_header)

non_actions = 28
attacker_actions = 4

# filename = "/home/ckinneer/PycharmProjects/apt-code/interp_results/out.nash.merged.csv"
filename = "/home/ckinneer/PycharmProjects/apt-code/interp_results/out.stackelberg.0.csv"

with open(filename) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",")
    line_count = 0
    for row in csv_reader:
        defender_actions = len(row) - non_actions - attacker_actions
        if line_count == -1:
            print(", ".join(row))
            line_count += 1
        else:
            try:
                rowsize = len(row)
                outline = row[0:non_actions-1+attacker_actions]

                defender = row[non_actions-1+attacker_actions:-1]

                wait = active = pas = 0
                for action in range(len(defender)):
                    parsed = parse_defender_actions(action)
                    wait += parsed[0] * float(defender[action])
                    if parsed[2] > -1:
                        active += float(defender[action])
                    if parsed[1] == 3:
                        pas += float(defender[action])

                outline.append(str(wait))
                outline.append(str(active))
                outline.append(str(pas))

                outline.append(row[-1])

                print(",".join(outline))
            except ValueError:
                print("WARNING ERROR! SKIPPED ROW: "+", ".join(row))

