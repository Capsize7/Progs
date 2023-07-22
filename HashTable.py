'''
Найти все вхождения строки Pattern в строку Text.
'''

import sys


class HashSearch:
    def __init__(self, text, pattern, p=None, x=None):
        self.p = 1_000_000_007 if p is None else p
        self.x = (self.p // 2) + 3 if x is None else x
        self.text = text
        self.pattern = pattern
        self.text_len = len(self.text)
        self.pattern_len = len(self.pattern)
        self.degrees = [None] * self.pattern_len
        x_deg = 1
        for i in range(self.pattern_len):
            self.degrees[i] = x_deg
            x_deg = (x_deg * self.x) % self.p
        self.hash_mem_sum = 0
        self.curr_idx = None
        self.ans = []
        self.hash_init()
        self.pattern_hash = self.hash_calc(self.pattern)

    def hash_calc(self, elem):
        ans = 0
        for i in reversed(range(self.pattern_len)):
            ans += (ord(elem[i]) * self.degrees[i]) % self.p
            ans = ans % self.p
        return ans

    def hash_init(self):
        self.curr_idx = self.text_len - self.pattern_len
        for i in reversed(range(self.pattern_len)):
            self.hash_mem_sum += (ord(self.text[self.curr_idx + i]) * self.degrees[i]) % self.p
            self.hash_mem_sum = self.hash_mem_sum % self.p

    def hash_move_recalculate(self):
        self.curr_idx -= 1
        idx_end_elem = self.curr_idx + self.pattern_len
        last_elem_sum = (ord(self.text[idx_end_elem]) * self.degrees[-1])
        self.hash_mem_sum -= last_elem_sum
        self.hash_mem_sum = self.hash_mem_sum % self.p
        self.hash_mem_sum *= self.x
        self.hash_mem_sum = self.hash_mem_sum % self.p
        new_elem_sum = (ord(self.text[self.curr_idx])) * self.degrees[0]
        self.hash_mem_sum += new_elem_sum
        self.hash_mem_sum = self.hash_mem_sum % self.p

    def is_equal_to_pattern(self, idx_start):
        if self.pattern == self.text[idx_start:idx_start + self.pattern_len]:
            return True
        else:
            return False
        for i in range(self.pattern_len):
            if self.pattern[i] != self.text[idx_start + i]:
                return False
        return True

    def find_all(self):

        while True:
            if self.hash_mem_sum == self.pattern_hash:
                if True or self.is_equal_to_pattern(self.curr_idx):
                    self.ans.append(self.curr_idx)
            if self.curr_idx == 0:
                return reversed(self.ans)
            else:
                self.hash_move_recalculate()


def main():
    pattern = sys.stdin.readline().strip()
    text = sys.stdin.readline().strip()
    src = HashSearch(text=text, pattern=pattern)
    ans = src.find_all()
    for i in ans:
        sys.stdout.write(str(i) + " ")


if __name__ == "__main__":
    main()
    data_example = ['aba', 'abacaba']
