"""
Реализуйте декоратор @recviz, который полностью визуализирует выполнение декорируемой функции, в том числе и рекурсивной.
Декоратор должен отображать все рекурсивные вызовы и возвращаемые значения, полученные при этих вызовах,
причем рекурсивные вызовы, выполняемые в глубину, должны отделяться друг от друга четырьмя пробелами.
Очередной вызов декорируемой функции при визуализации должен включать в себя знак ->,
имя декорируемой функции и аргументы, переданные при этом вызове.
 Возвращаемое значение при визуализации должно включать в себя знак <- и непосредственно само возвращаемое значение.
"""
import functools


def recviz(func):
    level = -1

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        nonlocal level
        level += 1

        pos_args = list(map(repr, args))
        keyword_args = [f'{k}={v!r}' for k, v in kwargs.items()]

        print('    ' * level + '->', f'{func.__name__}({", ".join(pos_args + keyword_args)})')
        value = func(*args, **kwargs)
        print('    ' * level + '<-', repr(value))

        level -= 1
        return value

    return wrapper


if __name__ == '__main__':
    @recviz
    def fib(n):
        if n <= 2:
            return 1
        else:
            return fib(n - 1) + fib(n - 2)


    fib(4)
