import re
import subprocess
import threading
import time


class tc(threading.Thread):

    def __init__(self, callback):
        """Form the monitor and register the monitored metrics."""
        super(tc, self).__init__()
        self.stop_flag = False
        self.interval = None
        self.net_if = None
        self.pattern = re.compile('(.*)backlog(.+)b( +)(.+)p(.*)', flags=re.DOTALL)
        self.callback = callback

        self.callback.add('network', 'queue')

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

    def run(self):
        """Monitor the metrics."""
        if not self.interval or not self.net_if:
            raise RuntimeError

        while not self.stop_flag:
            queue_size = self._get_queue_size()
            if queue_size is not None:
                self.callback.set_metric('network', 'queue', queue_size)

            time.sleep(self.interval)

        self.callback.remove('network', 'queue')
        
    def _get_queue_size(self):
        """Parse tc output and return the network interface queue size."""
        process_parameters = ['tc', '-s', 'qdisc', 'show', 'dev', self.net_if]
        tc_subprocess = subprocess.Popen(process_parameters,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE)
        output = ''
        output += tc_subprocess.stdout.readline().decode('ascii')
        output += tc_subprocess.stdout.readline().decode('ascii')
        output += tc_subprocess.stdout.readline().decode('ascii')
        
        match = self.pattern.match(output)
        
        if match is not None:
            return float(match.group(4));
        else:
            print('tc: Please check your network interface settings.')
            return None
