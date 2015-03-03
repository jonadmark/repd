import diagnostic


class pfitscher_network:
    def __init__(self, metric_manager):
        """Form the diagnoser"""
        self.mm = metric_manager
        self.t_queue_high = 0.0
        self.t_tr_high = 5.0

    def diagnose(self, interval):
        """Perform the diagnostic and return it"""
        v_queue_mean = self.mm.get_reduced_metric('network',
                                                        'queue',
                                                        ('mean', ),
                                                        interval)
        v_tr_stdev = self.mm.get_reduced_metric('network',
                                                      'transmission_rate',
                                                      ('stdev', ),
                                                      interval)
        v_tr_mean = self.mm.get_reduced_metric('network',
                                                     'transmission_rate',
                                                     ('mean', ),
                                                     interval)
        if v_tr_stdev is not None and v_tr_mean is not None:
            if v_tr_mean != 0.0:
                v_tr_cv = v_tr_stdev / v_tr_mean
            else:
                v_tr_cv = float('inf')
        else:
            v_tr_cv = None


        diag = diagnostic.Diagnostic(diagnoser='pfitscher_network',
                                     resource='network')

        if v_queue_mean is None or v_tr_cv is None:
            diag.diagnostic = None
        elif v_queue_mean > self.t_queue_high:
            diag.diagnostic = diagnostic.UNDER
        elif v_tr_cv > self.t_tr_high:
            diag.diagnostic = diagnostic.OVER
        else:
            diag.diagnostic = diagnostic.CORRECT
        
        if diag.diagnostic is not None:
            diag.info = self.make_info(v_queue_mean, v_tr_cv)
        return diag

    def make_info(self, v_queue_mean, v_tr_cv):
        """Generate a info message to the diagnostic"""
        info = '\n    - average queue size: %.2f packets'
        info += '\n    - CV for transmission rate: %.2f'
        return info % (v_queue_mean, v_tr_cv)