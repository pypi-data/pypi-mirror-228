# numequate/base.py

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b != 0:
        return a / b
    else:
        raise ValueError("Cannot divide by zero")

def power(base, exponent):
    return base ** exponent

def clamp(value, min_value, max_value):
    return max(min(value, max_value), min_value)

def lerp(start, end, alpha):
    return start + (end - start) * alpha

def map_range(value, in_min, in_max, out_min, out_max):
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min