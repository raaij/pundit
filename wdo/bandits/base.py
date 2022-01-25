from abc import ABC, abstractmethod


class BanditBase(ABC):
    def __init__(self, K, env, reporter=None, *args, **kwargs):
        self.arms = list(range(K))
        self.reporter = reporter
        self.env = env
        self.history = []

    def report(self, arm, reward):
        # TODO: Add _report abstractmethod
        # Maybe this shouln't be in bandit? We do want to report on bandit parameters, but it's not relevant
        # to the bandit algorithm itself.
        t = len(self.history) - 1
        if self.reporter:
            self.reporter.report(t, arm=arm, reward=reward)
        # self._report(t)

    @abstractmethod
    def get_action(self):
        raise NotImplementedError()

    def update(self, arm, reward):
        self.history.append([arm, reward])
        self.report(arm, reward)
        self._update(arm, reward)

    @abstractmethod
    def _update(self, arm, reward):
        raise NotImplementedError()
