import random
import numpy as np
import math

def sigmoid(x):
    return math.exp(x) / (math.exp(x) + 1)

class Environment:
    def __init__(self, θ, X, μ=sigmoid):
        self.θ = θ
        self.X = X
        self.μ = μ

        self.proba = [
            self.μ(np.dot(self.θ, self.X[action]))
            for action in range(self.number_of_actions)
        ]

    def do(self, action):
        return 1 if random.random() < self.proba[action] else 0

    @property
    def expected_reward(self):
        return self.proba

    @property
    def number_of_actions(self):
        return len(self.X)
