import math


def mean(lst):
    """Return the average of a float list."""
    length = len(lst)
    return sum(lst)/float(length) if length != 0 else None


def pstdev(lst):
    """Return the population standard deviation of a float list."""
    if len(lst) == 0:
        return None
    else:
        mean_squares = sum(list(map(lambda x: x**2, lst)))/float(len(lst))
        square_mean = (sum(lst)/float(len(lst)))**2
        return math.sqrt(float(mean_squares) - (square_mean))


def over(lst, threshold):
    """Return the percentage of values over the threshold of a float list."""
    if len(lst) == 0:
        return None
    else:
        return 100.0*len(list(filter(lambda x: x >= threshold, lst)))/float(len(lst))
