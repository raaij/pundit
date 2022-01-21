from abc import ABC, abstractmethod


class BanditBase(ABC):
    def __init__(self, K, env, *args, **kwargs):
        self.arms = list(range(K))
        self.env = env
        self.history = []

    @abstractmethod
    def get_action(self):
        raise NotImplementedError()

    def update(self, arm, reward):
        self.history.append([arm, reward])
        self._update(arm, reward)

    @abstractmethod
    def _update(self, arm, reward):
        raise NotImplementedError()
