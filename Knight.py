'''
Реализуйте класс Knight, описывающий шахматного коня.
'''


class Knight:
    def __init__(self, col, row, color):
        self.col = col
        self.row = row
        self.color = color

    def get_char(self):
        return 'N'

    def can_move(self, col, row):
        return (ord(self.col) - ord(col)) ** 2 + (self.row - row) ** 2 == 5

    def move_to(self, col, row):
        if self.can_move(col, row):
            self.col = col
            self.row = row

    def draw_board(self):
        for row in range(8, 0, -1):
            for col in 'abcdefgh':
                if self.col == col and self.row == row:
                    print(self.get_char(), end='')
                elif self.can_move(col, row):
                    print('*', end='')
                else:
                    print('.', end='')
            print()

if __name__ == '__main__':
    knight = Knight('c', 3, 'white')

    print(knight.row, knight.col)
    print(knight.can_move('e', 5))
    print(knight.can_move('e', 4))

    knight.move_to('e', 4)
    print(knight.row, knight.col)
    print('-'*8)
    knight = Knight('c', 3, 'white')

    knight.draw_board()