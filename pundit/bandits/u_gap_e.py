import math
from abc import abstractmethod

import numpy as np

from pundit.bandits.base import BanditBase


class UGapEBandit(BanditBase):
    def __init__(self, ϵ, m, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ϵ = ϵ
        self.m = m

        self.rewards = {arm: [] for arm in self.arms}

    def compute_round_parameters(self):
        betas = []
        lower_bounds = []
        upper_bounds = []
        regret_bounds = []

        for arm in self.arms:
            arm_beta = self.get_arm_beta(arm)
            betas.append(arm_beta)
            lower_bounds.append(self._compute_mean_reward(arm) - arm_beta)
            upper_bounds.append(self._compute_mean_reward(arm) + arm_beta)

        for k in set(self.arms):
            values = []
            for i in set(self.arms) - {arm}:
                values.append(upper_bounds[i] - lower_bounds[k])
            regret_bounds.append(max(values))

        return regret_bounds, lower_bounds, upper_bounds, betas

    def get_action(self):
        # Makes sure we have played every arm at least once
        for arm, rewards in self.rewards.items():
            if len(rewards) == 0:
                return arm

        B_t, L_t, U_t, β_t = self.compute_round_parameters()
        J_t = np.argsort(B_t)[::-1][: self.m]
        u_t, l_t = self._compute_u_t(J_t, U_t), self._compute_l_t(J_t, L_t)
        arm = u_t if β_t[u_t] > β_t[l_t] else l_t
        return arm

    @abstractmethod
    def get_arm_beta(self, arm):
        raise NotImplementedError()

    def _update(self, arm, reward):
        self.rewards[arm].append(reward)

    def _compute_l_t(self, J_t, L_t):
        l_t, l_t_value = None, None
        for arm in J_t:
            if not l_t_value or L_t[arm] > l_t_value:
                l_t = arm
                l_t_value = L_t[arm]
        return l_t

    def _compute_u_t(self, J_t, U_t):
        u_t, u_t_value = None, None
        for arm in set(self.arms) - set(J_t):
            if not u_t_value or U_t[arm] > u_t_value:
                u_t = arm
                u_t_value = U_t[arm]
        return u_t

    def _compute_mean_reward(self, arm):
        return np.mean(self.rewards[arm])


class UGapEBudgetBandit(UGapEBandit):
    def __init__(self, ϵ, m, n, a, *args, **kwargs):
        super().__init__(ϵ=ϵ, m=m, *args, **kwargs)
        self.n = n
        self.a = a

    def get_arm_beta(self, arm):
        # TODO: In our case, b = 1. This could be dynamically set.
        return math.sqrt(self.a / len(self.rewards[arm]))
