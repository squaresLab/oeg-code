import numpy as np
import random
import itertools
import scipy.misc
import matplotlib.pyplot as plt

# start attacker actions
RECON = 0
EXPLOIT = 1
STEAL = 2
KILL = 3


# start defender actions
OBSERVE = 0
EVICT = 1

#player names
ATTACKER = 0
DEFENDER = 1

class ServerObj():
    def __init__(self):
        self.presence = False
        self.discovered = False
        self.running = True
        self.links = []

    def new_child(self):
        child = ServerObj()
        child.links.append(self)
        self.links.append(child)

    def add_children(self, n):
        for i in range(n):
            self.new_child()

class gameObj():
    def __init__(self, coordinates, size, intensity, channel, reward, name):
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.size = size
        self.intensity = intensity
        self.channel = channel
        self.reward = reward
        self.name = name

class gameEnv():
    def __init__(self):
        self.servers = []
        self.presence = []
        self.discovered = []
        self.down = []
        self.turn = ATTACKER
        #plt.imshow(a, interpolation="nearest")

    def take_action(self, action):


