from rapidfuzz import fuzz


def compare_strings(result, target):
    return 1 - fuzz.ratio(result, target) / 100


def compare_numbers(result, target):
    abs_error = abs(result - target)
    rel_error = abs(abs_error / target)
    return abs_error, rel_error
