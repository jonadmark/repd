OVER = 0x123
UNDER = 0x456
CORRECT = 0X789


class Diagnostic:
    def __init__(self, diagnoser=None, resource=None,
                 diagnostic=None, info=None):
        """Form a diagnostic"""
        self.diagnoser = diagnoser
        self.resource = resource
        self.diagnostic = diagnostic
        self.info = info

    def __str__(self):
        """Form and return a string representation of the diagnostic"""
        if not self.diagnostic:
            return '{0} could not be diagnosed by {1}.'.format(self.resource,
                                                               self.diagnoser)
        else:
            switch = {
                OVER: 'OVERPROVISIONED',
                UNDER: 'UNDERPROVISIONED',
                CORRECT: 'CORRECT'
            }
            message = '=== %s ===\ndiagnostic: %s\ndiagnoser: %s\ninfo: %s\n'

            return message % (self.resource.upper(),
                              switch[self.diagnostic],
                              self.diagnoser,
                              self.info)
