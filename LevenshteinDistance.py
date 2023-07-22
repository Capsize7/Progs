'''
Вычислите расстояние редактирования двух данных непустых строк длины не более 10^2,
содержащих строчные буквы латинского алфавита.
'''
def main():
    word1, word2 = '_' + input().strip(), '_' + input().strip()
    m, n = len(word1), len(word2)
    arr = [j for j in range(m)]
    for i in range(1, n):
        for j in range(m):
            dist = i if j == 0 else min(arr[j - 1] + 1, arr[j] + 1, mem + int(word1[j] != word2[i]))
            mem = arr[j]
            arr[j] = dist
    print(dist)

if __name__ == '__main__':
    main()
    data_example = ['short', 'ports']

