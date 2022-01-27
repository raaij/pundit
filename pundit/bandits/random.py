import random

from pundit.bandits import BanditBase


class RandomBandit(BanditBase):
    def get_action(self):
        return random.choice(self.arms)

    def _update(self, arm, reward):
        pass
