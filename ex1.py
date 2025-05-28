def strict(func):
    def wrapper(*args, **kwargs):
        annotations = func.__annotations__
        for name, value in zip(func.__code__.co_varnames, args):
            if name in annotations and not isinstance(value, annotations[name]):
                raise TypeError(f"{name} must be {annotations[name]}")
        return func(*args, **kwargs)
    return wrapper


@strict
def sum_two(a: int, b: int) -> int:
    return a + b


print(sum_two(1, 2))  # >>> 3
print(sum_two(1, 2.4))  # >>> TypeError