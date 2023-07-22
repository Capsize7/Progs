'''
Построить in-order, pre-order и post-order обходы данного двоичного дерева
'''

import sys


def in_order_traverse(root_node):
    if root_node != -1:
        yield from in_order_traverse(tree[root_node][1])
        yield tree[root_node][0]
        yield from in_order_traverse(tree[root_node][2])


def pre_order_traverse(root_node):
    if root_node != -1:
        yield tree[root_node][0]
        yield from pre_order_traverse(tree[root_node][1])
        yield from pre_order_traverse(tree[root_node][2])


def post_order_traverse(root_node):
    if root_node != -1:
        yield from post_order_traverse(tree[root_node][1])
        yield from post_order_traverse(tree[root_node][2])
        yield tree[root_node][0]


if __name__ == "__main__":
    n = int(next(sys.stdin))
    tree = [list(map(int, line.split())) for line in sys.stdin]
    print(*in_order_traverse(0))
    print(*pre_order_traverse(0))
    print(*post_order_traverse(0))
    data_example = ['5', '4 1 2', '2 3 4', '5 -1 -1', '1 -1 -1', '3 -1 -1']
