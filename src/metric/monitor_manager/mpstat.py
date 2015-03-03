import threading
import time
import subprocess


class mpstat(threading.Thread):

    def __init__(self, callback):
        """Form the monitor and register the monitored metrics."""
        super(mpstat, self).__init__()
        self.stop_flag = False
        self.interval = None
        self.callback = callback

        self.callback.add('cpu', 'inuse')
        self.callback.add('cpu', 'steal')

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

        # open mpstat as a subprocess
        process_parameters = ['mpstat', str(self.interval)]
        try:
            mpstat_subprocess = subprocess.Popen(process_parameters,
                                                 stdout=subprocess.PIPE,
                                                 stderr=subprocess.PIPE)
        except:
            print('Could not create mpstat monitor, check if the sysstat package is installed in your system.')
            return

        # discard prelude
        mpstat_subprocess.stdout.readline()
        mpstat_subprocess.stdout.readline()

        # get column numbers
        output_line = mpstat_subprocess.stdout.readline().decode('ascii')
        output_line_columns = output_line.split()
        idle_col = output_line_columns.index('%idle')
        steal_col = output_line_columns.index('%steal')

        while mpstat_subprocess.poll() is None and not self.stop_flag:
            # read one line from the output
            output_line = mpstat_subprocess.stdout.readline().decode('ascii')
            output_line_columns = output_line.split()

            # in_use = 100.0 - %idle
            # (%idle: 12th column in line)
            idle = float(output_line_columns[idle_col].replace(',', '.'))
            inuse = 100.0 - idle
            self.callback.set_metric('cpu', 'inuse', inuse)

            # steal = %steal
            # (%steal: 9th column in line)
            steal = float(output_line_columns[steal_col].replace(',', '.'))
            self.callback.set_metric('cpu', 'steal', steal)

            # sleep some time
            time.sleep(self.interval)

        #if mpstat_subprocess.poll() is not None:
        #    mpstat_subprocess.terminate()

        self.callback.remove('cpu', 'inuse')
        self.callback.remove('cpu', 'steal')
