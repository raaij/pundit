import math
import random
import itertools
import json
import pandas as pd
from typing import List, Dict, Tuple

import numpy as np

from pundit.interface.apps.experiment.input import (
    INPUT_EXPERIMENT_NAME, INPUT_HEADER_COUNT, INPUT_DESCRIPTION_COUNT, \
    INPUT_IMAGE_COUNT, INPUT_CONFIDENCE, INPUT_BUDGET)
from pundit.core.environment import Environment
from pundit.core.ml.u_gap_e import UGapEc
from pundit.constant import PATH_DATA_RESULT

DEFAULT_DELTA = 0.1
DEFAULT_C = 0.5
DEFAULT_M = 1


class Experiment:
    def __init__(self, name, asset, n_asset, confidence=95, budget=None):
        self.name = name
        self.asset = asset
        self.n_asset = n_asset
        self.confidence = confidence
        self.budget = budget

        self.env = None
        self.bandit = None
        self.designs = None
        self.opt = None
        self.B_opt = None
        self.data = None

    @classmethod
    def from_input(cls, path):
        with open(path, 'r') as fp:
            config = json.load(fp)

        budget = config[INPUT_BUDGET]
        if budget:
            budget = int(budget)
        else:
            budget = 100_000

        return cls(
            name=config[INPUT_EXPERIMENT_NAME],
            asset=['header', 'description', 'image'],
            n_asset=[
                int(config[INPUT_HEADER_COUNT]),
                int(config[INPUT_DESCRIPTION_COUNT]),
                int(config[INPUT_IMAGE_COUNT])
            ],
            confidence=float(config[INPUT_CONFIDENCE]),
            budget=budget
        )

    def configure(self):
        n_h, n_d, n_i = self.n_asset

        θ = np.array([
            random.gauss(-1, 0.2)
            , *[random.gauss(0, 0.5) for _ in range(n_h + n_i + n_d)]
        ])
        self.designs = []
        X = []
        for h, d, i in itertools.product(*[range(n) for n in [n_h, n_d, n_i]]):
            combination = [0 for _ in range(n_h + n_i + n_d + 1)]
            combination[0] = 1
            combination[1 + h] = 1
            combination[1 + n_h + d] = 1
            combination[1 + n_h + n_d + i] = 1
            X.append(np.array(combination))
            self.designs.append([h, d, i])

        self.env = Environment(θ, X)
        print()
        self.bandit = UGapEc(
            ϵ=1 - (0.01 * self.confidence),
            δ=DEFAULT_DELTA,
            m=DEFAULT_M,
            c=DEFAULT_C,
            env=self.env
        )

    def run(self):
        data = []
        for t in range(1, self.budget + 1):
            # Stop condition
            if t > 200:
                if np.any([b < self.bandit.ϵ for b in self.bandit.B]):
                    break

            action, reward = self.bandit.play_round()
            row = {
                't': t,
                'action': action,
                'reward': reward,
                'header': self.designs[action][0],
                'description': self.designs[action][1],
                'image': self.designs[action][2],
            }
            row['B_action'] = None if t < 200 else self.bandit.B[action]

            data.append(row)

        self.opt = np.argmin(self.bandit.B)
        self.B_opt = np.min(self.bandit.B)
        self.data = pd.DataFrame(data)

    def save(self):
        self.data.to_csv(PATH_DATA_RESULT / self.name / 'result.csv')
