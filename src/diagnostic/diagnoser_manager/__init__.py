


class DiagnoserManager:
    def __init__(self, metric_manager, diagnosers):
        """Form a DiagnoserManager.

        Arguments:
        metric_manager -- a reference to a MetricManager
        diagnosers -- list of diagnoser names
        """
        self.metric_manager = metric_manager
        self.diagnosers = {}

        for diagnoser in diagnosers:
            self.add(diagnoser)

    def add(self, diagnoser_id):
        """Add a diagnoser to be managed."""
        if diagnoser_id not in self.diagnosers:
            module = __import__(__name__+'.'+diagnoser_id, globals(),
                                locals(), [diagnoser_id], 0)
            diagnoser = getattr(module, diagnoser_id)
            self.diagnosers[diagnoser_id] = diagnoser(self.metric_manager)
        else:
            raise KeyError

    def remove(self, diagnoser_id):
        """Remove a managed diagnoser."""
        del self.diagnosers[diagnoser_id]

    def diagnose(self, interval):
        """Make diagnosers diagnose and return a list of their diagbostics."""
        diagnostics = []
        for id in sorted(self.diagnosers):
            diagnostics.append(self.diagnosers[id].diagnose(interval))
        return diagnostics
