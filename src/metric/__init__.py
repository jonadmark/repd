


class Metric:
    def __init__(self):
        """Form a metric"""
        self.value = None

    def set(self, value):
        self.value = value

    def get(self):
        return self.value

    def reset(self):
        self.value = None

    def is_updated(self):
        """Inform if metric is updated"""
        return self.value is not None
