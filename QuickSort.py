"""
В первой строке задано два целых числа 'n' и 'm' — количество отрезков и точек на прямой, соответственно.
Следующие 'n' строк содержат по два целых чисел числа 'ai', и 'bi'
'ai' < 'bi' — координаты концов отрезков. Последняя строка содержит 'm' целых чисел — координаты точек.
Точка считается принадлежащей отрезку, если она находится внутри него или на границе.
Для каждой точки в порядке появления во вводе выведите, скольким отрезкам она принадлежит.
"""
def partition(a):
    lss, eql, grt = [], [], []
    pvt = (a[0] + a[len(a)//2] + a[-1])//3
    for x in a:
        if x < pvt:
            lss.append(x)
        elif x == pvt:
            eql.append(x)
        else:
            grt.append(x)
    return lss, eql, grt


# Быстрая сортировка с элиминацией хвостовой рекурсии


def quicksort(a):
    while len(a) > 1:
        lss, eql, grt = partition(a)
        if len(lss) < len(grt):
            first = quicksort(lss)
            return first + eql + quicksort(grt)
        elif len(lss) > len(grt):
            first = quicksort(grt)
            return quicksort(lss) + eql + first
        else:
            return quicksort(lss) + eql + quicksort(grt)
    return a


# Кол-во элементов слева от x (n - нестрогое/строгое неравенство)


def binarycount(lst, x, n):
    l, r = 0, len(lst) - 1
    while l <= r:
        m = l + (r - l) // 2
        if lst[m] <= x - n:
            l = m + 1
        elif lst[m] > x - n:
            r = m - 1
    return l


def main():
    left, right = [], []
    n, m = map(int, input().split())
    for i in range(n):
        l, r = map(int, input().split())
        left.append(l)
        right.append(r)
    point = [int(i) for i in input().split()]
    left, right = quicksort(left), quicksort(right)
    for i in point:
        print(binarycount(left, i, 0) - binarycount(right, i, 1), end=' ')

if __name__ == '__main__':
    main()
    data_example = ['2 3', '0 5', '7 10', '1 6 10']