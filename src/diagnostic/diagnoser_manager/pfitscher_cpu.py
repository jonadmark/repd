import diagnostic


class pfitscher_cpu:
    def __init__(self, metric_manager):
        """Form the diagnoser"""
        self.mm = metric_manager
        self.t_inuse_high = 80.0
        self.t_inuse_low = 50.0
        self.t_inuse_saturated = 20.0
        self.t_steal_high = 1.0

    def diagnose(self, interval):
        """Perform the diagnostic and return it"""
        v_inuse_mean = self.mm.get_reduced_metric('cpu',
                                                        'inuse',
                                                        ('mean', ),
                                                        interval)
        v_inuse_over = self.mm.get_reduced_metric('cpu',
                                                        'inuse',
                                                        ('over',95.0),
                                                        interval)
        v_steal_mean = self.mm.get_reduced_metric('cpu',
                                                        'steal',
                                                        ('mean', ),
                                                        interval)

        diag = diagnostic.Diagnostic(diagnoser='pfitscher_cpu',
                                     resource='cpu')

        if v_inuse_mean is None or v_steal_mean is None:
            diag.diagnostic = None
        elif v_steal_mean >= self.t_steal_high \
                or v_inuse_mean >= self.t_inuse_high:
            diag.diagnostic = diagnostic.UNDER
        elif v_inuse_mean < self.t_inuse_low \
                and v_inuse_over <= self.t_inuse_saturated:
            diag.diagnostic = diagnostic.OVER
        else:
            diag.diagnostic = diagnostic.CORRECT

        if diag.diagnostic is not None:
            diag.info = self.make_info(v_inuse_mean, v_inuse_over, v_steal_mean)
        return diag

    def make_info(self, v_inuse_mean, v_inuse_over, v_steal_mean):
        """Generate a info message to the diagnostic"""
        info = '\n    - average utilization: %.2f%%'
        info += '\n    - utilization above 95%%: %.2f%%'
        info += '\n    - average steal: %.2f%%'
        return info % (v_inuse_mean, v_inuse_over, v_steal_mean)

