import json
import random

from wdo.bandits import EpsilonGreedyBandit
from wdo.constant import PATH_RESULTS
from wdo.env import WebsiteEnvironmentSimple
from wdo.reporter import Reporter

N_IMPRESSIONS = 10_000


class Experiment:
    def __init__(self, env_klass, bandit_klass, params):
        self.env = env_klass(**params)
        self.reporter = Reporter()
        self.bandit = bandit_klass(env=self.env, reporter=self.reporter, **params)
        self.name = params['name']

    @classmethod
    def from_config(cls, config_path):
        with open(config_path, 'r') as fp:
            config = json.load(fp)

        # TODO: Remove this, should be set in config
        K = 8
        proba = [0.05 + random.random() * 0.10 for _ in range(K)]
        return cls(
            env_klass=WebsiteEnvironmentSimple,
            bandit_klass=EpsilonGreedyBandit,
            params={
                'K': K,
                'proba': proba,
                'ε': 0.1,
                'name': config_path.as_uri().split('/')[-1].replace('.json', '')
            }
        )

    def run(self):
        for _ in range(N_IMPRESSIONS):
            action = self.bandit.get_action()
            reward = self.env.do(action)
            self.bandit.update(action, reward)

    def save(self):
        import pandas as pd
        data = pd.DataFrame.from_dict(self.reporter.history, orient='index')
        data = data.reset_index()
        data.columns = ['time', 'arm', 'reward']
        data.to_csv(PATH_RESULTS / (self.name + '.csv'))
