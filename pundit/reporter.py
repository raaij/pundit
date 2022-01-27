class Reporter:
    def __init__(self):
        self.history = {}

    def report(self, t, *args, **kwargs):
        if not t in self.history:
            self.history[t] = {}

        for key, value in kwargs.items():
            self.history[t][key] = value

