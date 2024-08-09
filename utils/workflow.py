class Workflow:
    def __init__(self, engine):
        self.engine = engine
        self.workflow = []

    def add_step(self, step, *args):
        self.workflow.append((step, args))

    def run(self):
        for step, args in self.workflow:
            step(*args)
