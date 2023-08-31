# numequate/utils.py

def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)

def math(expression):
    try:
        result = eval(expression)
        return result
    except Exception as e:
        return f"Error: {str(e)}"