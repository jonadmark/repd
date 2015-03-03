import diagnostic


class pfitscher_memory:
    def __init__(self, metric_manager):
        """Form the diagnoser"""
        self.mm = metric_manager
        self.t_resident_low = 50.0
        self.t_resident_high = 70.0
        self.t_committed_relevant = 150.0

    def diagnose(self, interval):
        """Perform the diagnostic and return it"""
        v_resident_mean = self.mm.get_reduced_metric('memory',
                                                           'resident',
                                                           ('mean', ),
                                                           interval)
        v_committed_mean = self.mm.get_reduced_metric('memory',
                                                            'committed',
                                                            ('mean', ),
                                                            interval)

        diag = diagnostic.Diagnostic(diagnoser='pfitscher_memory',
                                     resource='memory')

        if v_resident_mean is None or v_committed_mean is None:
            diag.diagnostic = None
        elif v_resident_mean < self.t_resident_low\
                and v_committed_mean < self.t_committed_relevant:
            diag.diagnostic = diagnostic.OVER
        elif (v_resident_mean >= self.t_resident_low
                and v_committed_mean >= self.t_committed_relevant)\
                or (v_resident_mean >= self.t_resident_high
                and v_committed_mean < self.t_committed_relevant):
            diag.diagnostic = diagnostic.UNDER
        else:
            diag.diagnostic = diagnostic.CORRECT

        if diag.diagnostic is not None:
            diag.info = self.make_info(v_resident_mean, v_committed_mean)
        return diag

    def make_info(self, v_resident_mean, v_committed_mean):
        """Generate a info message to the diagnostic"""
        info = '\n    - average resident: %.2f%%'
        info += '\n    - average committed: %.2f%%'
        return info % (v_resident_mean, v_committed_mean)
