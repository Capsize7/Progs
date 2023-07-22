'''
Первая строка входа содержит целые числа 'W' и 'n' — вместимость рюкзака и число золотых слитков.
Следующая строка содержит 'n' целых чисел, задающих веса слитков.
Найдите максимальный вес золота, который можно унести в рюкзаке.
'''
from functools import lru_cache


@lru_cache(None)
def sack(i, j):
    if i < 0 or j < 1:
        return 0

    return max(sack(i - 1, j), sack(i - 1, j - w[i]) + w[i] if j >= w[i] else 0)


if __name__ == '__main__':
    W, n = map(int, input().split())
    w = list(map(int, input().split()))
    print(sack(len(w) - 1, W))
    data_example = ['10 3', '1 4 8']
