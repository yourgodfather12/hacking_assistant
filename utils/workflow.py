import logging

logger = logging.getLogger(__name__)

class Workflow:
    def __init__(self, engine):
        """Initialize a workflow with the specified engine."""
        self.engine = engine
        self.workflow = []

    def add_step(self, step, *args):
        """Add a step to the workflow."""
        self.workflow.append((step, args))
        logger.info(f"Added step {step.__name__} to workflow.")

    def run(self):
        """Run the workflow."""
        for step, args in self.workflow:
            try:
                step(*args)
                logger.info(f"Executed step {step.__name__} in workflow.")
            except Exception as e:
                logger.error(f"Error executing step {step.__name__} in workflow: {e}")
