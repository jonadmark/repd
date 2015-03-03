import threading
import time
import re


class procnetdev(threading.Thread):

    def __init__(self, callback):
        """Form the monitor and register the monitored metrics."""
        super(procnetdev, self).__init__()
        self.stop_flag = False
        self.interval = None
        self.net_if = None
        self.callback = callback

        self.callback.add('network', 'transmission_rate')

    def stop(self):
        """Prepare monitor to stop."""
        self.stop_flag = True

    def set(self, argument, value):
        """Set a monitor argument.

        Arguments:
        argument -- arugment name
        value -- value for the argument
        """
        if argument == 'interval':
            self.interval = value
        elif argument == 'interface':
            self.net_if = value
            pat = '(.*)(\A|\s)'+self.net_if+':( *)(.+?)\n(.*)'
            self.pattern = re.compile(pat, flags=re.DOTALL)

    def run(self):
        """Monitor the metrics."""
        if not self.interval or not self.net_if:
            raise RuntimeError

        prev_transmitted_n_bytes = self._get_column_value(8)
        while not self.stop_flag:
            time.sleep(self.interval)
            cur_transmitted_n_bytes = self._get_column_value(8)

            if prev_transmitted_n_bytes is not None and \
                    cur_transmitted_n_bytes is not None:
                diff_cur_prev = cur_transmitted_n_bytes - prev_transmitted_n_bytes
                transmission_rate = diff_cur_prev / self.interval
                self.callback.set_metric('network',
                                         'transmission_rate',
                                         transmission_rate)

            prev_transmitted_n_bytes = cur_transmitted_n_bytes

        self.callback.remove('network', 'transmission_rate')

    def _get_column_value(self, column_number):
        """Parse pseudo-file and return the value of the column.

        Arguments:
        column_number -- number of the column to return the value
        """
        with open('/proc/net/dev', 'r') as pnd:
            pnd_content = pnd.read()

        ln = self.pattern.match(pnd_content)
        if ln is not None:
            lns = ln.group(4).split()
            return float(lns[column_number])
        else:
            print('procnetdev: Please check your network interface settings.')
            return None
