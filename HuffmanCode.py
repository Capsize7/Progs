'''
По данной непустой строке 's' длины не более 10^4,
состоящей из строчных букв латинского алфавита, постройте оптимальный беспрефиксный код.
В первой строке выведите количество различных букв 'k',
встречающихся в строке, и размер получившейся закодированной строки.
В следующих 'k' строках запишите коды букв в формате "letter: code".
В последней строке выведите закодированную строку.
'''
import collections

def popmin(tree, codes, num):
    el = tree.pop(tree.index(min(tree)))
    for s in el[1]:
        codes[s] = num + codes[s]
    return el[0], el[1]


def main(sss):
    count = collections.Counter(sss)
    codes = dict.fromkeys(count, '0' if len(count) == 1 else '')
    tree = [[count[key], key] for key in count]
    while len(tree) > 1:
        val1, s1 = popmin(tree, codes, '0')
        val2, s2 = popmin(tree, codes, '1')
        tree.append([val1 + val2, s1 + s2])
    word = ''.join(codes[s] for s in sss)
    print(len(count), len(word))
    [print('{}: {}'.format(k, codes[k])) for k in sorted(codes)]
    print(word)


if __name__ == '__main__':
    main('abacabad')