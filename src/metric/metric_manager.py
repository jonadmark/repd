import threading
import time
from metric import Metric
from metric import statistics


class MetricManager:
    def __init__(self, database):
        """Form a MetricManager

        Arguments:
        database -- a reference to a Database
        """
        self.metrics = {}
        self.database = database
        self.lock = threading.Lock()

    def add(self, resource, metric):
        """Add a metric to be managed"""
        with self.lock:
            if resource not in self.metrics:
                self.metrics[resource] = {}
            self.metrics[resource][metric] = Metric()

    def remove(self, resource, metric):
        """Remove a managed metric"""
        with self.lock:
            del self.metrics[resource][metric]
            if len(self.metrics[resource]) == 0:
                del self.metrics[resource]

    def set_metric(self, resource, metric, value):
        """Find out the current timestamp and insert the metric value on the 
        database with it.

        Arguments:
        resource -- the resource name related to the metric
        metric -- the metric name
        value -- the value which was collected
        """
        with self.lock:
            self.metrics[resource][metric].set(value)
            if self._resource_is_updated(resource):
                timestamp = int(time.time())
                for metric in self.metrics[resource]:
                    self.database.insert(timestamp, resource, metric,
                                         self.metrics[resource][metric].get())
                    self.metrics[resource][metric].reset()

    def get_reduced_metric(self, resource, metric, reduce, interval):
        """Reduce the metric values within an interval.

        Arguments:
        resource -- the resource name related to the metric
        metric -- the metric name
        reduce -- the reduce function name (i.e. stdev)
        interval -- a tuple of timestamps (begin, end)
        """
        raw_list = self.database.get_values_interval(resource, metric, interval)
        if raw_list is None:
            return None
        float_list = list(map(lambda x: float(x[2]), raw_list))

        if reduce[0] == 'mean':
            return statistics.mean(float_list)
        elif reduce[0] == 'stdev':
            return statistics.pstdev(float_list)
        elif reduce[0] == 'over':
            return statistics.over(float_list, reduce[1])
        else:
            raise KeyError

    def _resource_is_updated(self, resource):
        """Inform if a resource is updated considering all of its metrics."""
        for metric_id in self.metrics[resource]:
            if not self.metrics[resource][metric_id].is_updated():
                return False
        return True
