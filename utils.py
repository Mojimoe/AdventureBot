import numpy
import traceback
import datetime
import math
import copy


def log(message):
    print(">" + message)


def log_temp(message):
    print(">>>>>" + message)


def log_exception(exception):
    print(traceback.format_exc())


def lerp(a, b, alpha):
    return ((1-alpha) * a) + (alpha * b)


def floor(val):
    return math.floor(val)


def clamp(val, minimum, maximum):
    return min(max(val, minimum), maximum)


def normalize_list(list):
    # Makes sure a list sums to one by dividing every element.

    list_sum = sum(list)
    return [x / list_sum for x in list]


def chance(in_ratio):
    # Returns TRUE a fraction of the time.

    true_probability = max(0, min(1, in_ratio))
    false_probability = 1 - true_probability

    return numpy.random.choice([True, False], p=[true_probability, false_probability])


def select(list):
    return numpy.random.choice(list)


def select_with_weight(list, weight_list):
    # Selects from a list, given a weight list.
    # The weight list does not need to be normalized.

    normalized_weight_list = normalize_list(weight_list)

    return numpy.random.choice(list, p=normalized_weight_list)


def multiselect_with_weight(list, weight_list, elements):
    # Selects from a list, returns a list of elements

    normalized_weight_list = normalize_list(weight_list)

    return numpy.random.choice(list, elements, p=normalized_weight_list, replace=False)


def shuffle(list):
    # Shuffles in-place
    numpy.random.shuffle(list)


def randfloat(minimum, maximum):
    return lerp(minimum, maximum, numpy.random.random())


def randint(minimum, maximum):
    return round(randfloat(minimum, maximum))


def now():
    return datetime.datetime.utcnow()


def get_future_timestamp(days=0, hours=0, minutes=0, seconds=0):
    return datetime.datetime.utcnow() + datetime.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)


def clone(object):
    # Returns a copy of the object.
    return copy.copy(object)
