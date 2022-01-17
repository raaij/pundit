import random

import numpy as np

from bandits.base import BanditBase


class EpsilonGreedyBandit(BanditBase):
    def __init__(self, ϵ, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ϵ = ϵ
        self.rewards = {arm: [] for arm in self.arms}

    def get_action(self):
        if random.random() < self.ϵ:
            action = random.choice(self.arms)
        else:
            action = np.argmax([np.mean(arm_rewards) for arm_rewards in self.rewards.values()])

        return action

    def _update(self, arm, reward):
        self.rewards[arm].append(reward)
