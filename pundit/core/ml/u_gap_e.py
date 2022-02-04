import math
from abc import abstractmethod

import numpy as np

# from pundit.ml.bandits.base import


class _UGapE:
    """
    TODO:
    - Use BanditBase
    """
    def __init__(self, ϵ, m, env, *args, **kwargs):
        # TODO: Make it work for more than 1 arm?
        assert m == 1

        self.ϵ = ϵ
        self.m = m
        self.env = env

        self.arms = list(range(env.number_of_actions))
        self._rewards = {arm: [] for arm in self.arms}

        for param in ['β', 'U', 'L', 'B', 'μ']:
            setattr(self, param, None)

        self.t = 1

    def play_round(self):
        action = self.get_action()
        reward = self.env.do(action)
        self.update(action, reward)
        return action, reward

    def get_action(self):
        # Check if any arm has not been pulled
        for arm in self.arms:
            if not len(self._rewards[arm]):
                return arm

        # Stop condition ?
        self.μ = np.array([np.mean(self._rewards[arm]) for arm in self.arms])
        T = np.array([len(self._rewards[arm]) for arm in self.arms])
        self.β = self.compute_β(T=T)
        self.L, self.U = self.μ - self.β, self.μ + self.β
        self.B = self.compute_B()

        J = np.argmin(self.B)
        l = J
        # TODO: Shorter code?
        u, u_value = None, None
        for arm in set(self.arms) - {J}:
            if u == None or self.U[arm] > u_value:
                u, u_value = arm, self.U[arm]

        I = l if self.β[l] >= self.β[u] else u
        return I

    def update(self, action, reward):
        self._rewards[action].append(reward)
        self.t += 1

    def compute_β(self, *args, **kwargs):
        raise NotImplementedError()

    def compute_B(self):
        # TODO - Make this more efficient?
        B = []
        for k in self.arms:
            B.append(max([
                self.U[i] - self.L[k] for i in set(self.arms) - {k}
            ]))
        return B


class UGapEb(_UGapE):
    def __init__(self, ϵ, m, n, a, *args, **kwargs):
        super().__init__(ϵ, m, *args, **kwargs)
        self.n = n
        self.a = a

    def compute_β(self, T, *args, **kwargs):
        b = 1  # TODO - Should be a parameter
        return b * np.sqrt(self.a / T)


class UGapEc(_UGapE):
    def __init__(self, ϵ, m, δ, c, *args, **kwargs):
        super().__init__(ϵ, m, *args, **kwargs)
        self.δ = δ
        self.c = c

    def compute_β(self, T, *args, **kwargs):
        b = 1  # TODO - Should be a parameter
        K = len(self.arms)

        return b * np.sqrt(
            (self.c * math.log((4 * K * (self.t - 1) ** 3) / self.δ)) /
            T
        )
import math
from abc import abstractmethod

import numpy as np

# from pundit.ml.bandits.base import


class _UGapE:
    """
    TODO:
    - Use BanditBase
    """
    def __init__(self, ϵ, m, env, *args, **kwargs):
        # TODO: Make it work for more than 1 arm?
        assert m == 1

        self.ϵ = ϵ
        self.m = m
        self.env = env

        self.arms = list(range(env.number_of_actions))
        self._rewards = {arm: [] for arm in self.arms}

        for param in ['β', 'U', 'L', 'B', 'μ']:
            setattr(self, param, None)

        self.t = 1

    def play_round(self):
        action = self.get_action()
        reward = self.env.do(action)
        self.update(action, reward)
        return action, reward

    def get_action(self):
        # Check if any arm has not been pulled
        for arm in self.arms:
            if not len(self._rewards[arm]):
                return arm

        # Stop condition ?
        self.μ = np.array([np.mean(self._rewards[arm]) for arm in self.arms])
        T = np.array([len(self._rewards[arm]) for arm in self.arms])
        self.β = self.compute_β(T=T)
        self.L, self.U = self.μ - self.β, self.μ + self.β
        self.B = self.compute_B()

        J = np.argmin(self.B)
        l = J
        # TODO: Shorter code?
        u, u_value = None, None
        for arm in set(self.arms) - {J}:
            if u == None or self.U[arm] > u_value:
                u, u_value = arm, self.U[arm]

        I = l if self.β[l] >= self.β[u] else u
        return I

    def update(self, action, reward):
        self._rewards[action].append(reward)
        self.t += 1

    def compute_β(self, *args, **kwargs):
        raise NotImplementedError()

    def compute_B(self):
        # TODO - Make this more efficient?
        B = []
        for k in self.arms:
            B.append(max([
                self.U[i] - self.L[k] for i in set(self.arms) - {k}
            ]))
        return B


class UGapEb(_UGapE):
    def __init__(self, ϵ, m, n, a, *args, **kwargs):
        super().__init__(ϵ, m, *args, **kwargs)
        self.n = n
        self.a = a

    def compute_β(self, T, *args, **kwargs):
        b = 1  # TODO - Should be a parameter
        return b * np.sqrt(self.a / T)


class UGapEc(_UGapE):
    def __init__(self, ϵ, m, δ, c, *args, **kwargs):
        super().__init__(ϵ, m, *args, **kwargs)
        self.δ = δ
        self.c = c

    def compute_β(self, T, *args, **kwargs):
        b = 1  # TODO - Should be a parameter
        K = len(self.arms)

        return b * np.sqrt(
            (self.c * math.log((4 * K * (self.t - 1) ** 3) / self.δ)) /
            T
        )
