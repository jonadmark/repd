import threading
import time
import re


class procmeminfo(threading.Thread):

    def __init__(self, callback):
        """Form the monitor and register the monitored metrics."""
        super(procmeminfo, self).__init__()
        self.stop_flag = False
        self.interval = None
        self.callback = callback

        self.callback.add('memory', 'resident')
        self.callback.add('memory', 'committed')

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

    def run(self):
        """Monitor the metrics."""
        if not self.interval:
            raise RuntimeError

        # compile search patterns from parameters
        compiled_patterns = {}
        columns = ['Committed_AS','MemTotal','MemFree','Buffers','Cached']
        for column in columns:
            pattern = '(.*)(\A|\s)'+column+':( *)(.+?)( *)kB(.*)'
            compiled_patterns[column] = re.compile(pattern, flags=re.DOTALL)

        while not self.stop_flag:
            # sleep some time
            time.sleep(self.interval)

            # read /proc/meminfo file
            with open('/proc/meminfo', 'r') as pm:
                procmeminfo_content = pm.read()

            mem_total = float(compiled_patterns['MemTotal'].match(
                procmeminfo_content).group(4))
            # resident = (MemTotal - MemFree - Buffers - Cached)*100.0/MemTotal
            mem_free = float(compiled_patterns['MemFree'].match(
                procmeminfo_content).group(4))
            buffers = float(compiled_patterns['Buffers'].match(
                procmeminfo_content).group(4))
            cached = float(compiled_patterns['Cached'].match(
                procmeminfo_content).group(4))
            resident = (mem_total - mem_free - buffers - cached)*100.0/mem_total
            self.callback.set_metric('memory', 'resident', resident)

            # committed = (Committed_AS * 100.0) / MemTotal
            committed_as = float(compiled_patterns['Committed_AS'].match(
                procmeminfo_content).group(4)) * 100.0 / mem_total
            self.callback.set_metric('memory', 'committed', committed_as)

        self.callback.remove('memory', 'resident')
        self.callback.remove('memory', 'committed')
