import json
import threading


class MonitorManager:
    def __init__(self, metric_manager, resources):
        """Form a MonitorManager.

        Arguments:
        metric_manager -- a reference to a MetricManager
        resources -- a list of monitor groups and arguments
        """
        self.metric_manager = metric_manager
        self.monitors = {}
        self.lock = threading.Lock()

        for resource in resources:
            for monitor in resource['monitors']:
                self.add(monitor['id'])
                for arg in monitor['args']:
                    self.set_monitor(monitor['id'], arg, resource['argv'][arg])

    def add(self, monitor_id):
        """Add a monitor to be managed."""
        with self.lock:
            if monitor_id not in self.monitors:
                module = __import__(__name__+'.'+monitor_id, globals(),
                                    locals(), [monitor_id], 0)
                monitor = getattr(module, monitor_id)
                self.monitors[monitor_id] = monitor(self.metric_manager)

    def remove(self, monitor_id):
        """Remove a managed monitor."""
        with self.lock:
            if self.monitors[monitor_id].is_running():
                self.monitors[monitor_id].stop()
                self.monitors[monitor_id].join()
            del self.monitors[monitor_id]

    def set_monitor(self, monitor_id, argument, value):
        """Set a monitor argument.

        Arguments:
        monitor_id -- the monitor identification
        argument -- arugment name
        value -- value for the argument
        """
        with self.lock:
            if not self.monitors[monitor_id].is_alive():
                self.monitors[monitor_id].set(argument, value)

    def start(self):
        """Start all monitors."""
        with self.lock:
            for monitor_id in self.monitors:
                if not self.monitors[monitor_id].is_alive():
                    try:
                        self.monitors[monitor_id].start()
                    except RuntimeError:
                        self.stop()
                        raise RuntimeError

    def stop(self):
        """Request stop and wait all monitors stop."""
        with self.lock:
            for monitor_id in self.monitors:
                if self.monitors[monitor_id].is_alive():
                    self.monitors[monitor_id].stop()
                    self.monitors[monitor_id].join()
