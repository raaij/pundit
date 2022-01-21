import random

REWARD_CLICK = 1
REWARD_NO_CLICK = 0


class WebsiteEnvironmentSimple:
    def __init__(self, proba, *args, **kwargs):
        self.proba = proba

    def do(self, action):
        reward = REWARD_CLICK if random.random() < self.proba[action] else REWARD_NO_CLICK
        return reward
