class TicTacToe:
    '''
    Игра крестики-нолики. Вводите координаты начиная с 1. Пример ввода координаты - "1 1"
    '''
    FREE_CELL = 0  # свободная клетка
    HUMAN_X = 1  # крестик (игрок - человек)
    COMPUTER_O = 2  # нолик (игрок - компьютер)

    def __init__(self):
        '''Инициализация'''
        self.pole = [[Cell() for _ in range(3)] for _ in range(3)]
        self.free_cells = 9
        self.winner = None
        self.diagonals = [[self.pole[i][i] for i in range(3)], [self.pole[-i - 1][i] for i in range(-3, 0)]]
        for diag in self.diagonals:
            for cell in diag:
                cell._priority += 2

    def __getitem__(self, coords):
        '''Геттер значения клетки по координатам'''
        if self._valid_coords(*coords):
            return self.pole[coords[0]][coords[1]].value
        raise IndexError('некорректно указанные индексы')

    def __setitem__(self, coords, value):
        '''Сеттер значения клетки по координатам'''
        if not self._valid_coords(*coords):
            raise IndexError('некорректно указанные индексы')
        if value in (0, 1, 2):
            self.pole[coords[0]][coords[1]].value = value
        self.__bool__()

    def __bool__(self):
        '''Проверка окончена игра или нет'''
        for row in self.pole:
            if not any(row) and len(set(row)) == 1:
                self.winner = row[0].value
                return False
        for col in zip(*self.pole):
            if not any(col) and len(set(col)) == 1:
                self.winner = col[0].value
                return False
        for diag in self.diagonals:
            if not any(diag) and len(set(diag)) == 1:
                self.winner = diag[0].value
                return False
        if self.free_cells == 0:
            self.winner = 0
            return False
        return True

    @property
    def is_human_win(self):
        return self.winner == self.HUMAN_X

    @property
    def is_computer_win(self):
        return self.winner == self.COMPUTER_O

    @property
    def is_draw(self):
        return self.winner == 0

    @classmethod
    def _valid_coords(cls, y, x):
        '''Проверка координат'''
        return type(y) == type(x) == int and 0 <= y < 3 and 0 <= x < 3

    def init(self):
        self.__init__()

    def human_go(self):
        '''Ход человека'''
        while True:
            print('Введите координаты свободной клетки через пробел:')
            coords = input()
            if len(coords.split()) != 2:
                print('Было введено неверное количество координат.')
                continue
            try:
                y, x = map(int, coords.split())
                y -= 1
                x -= 1
                if not self._valid_coords(y, x):
                    print('Введённые координаты вне диапазона поля.')
                    continue
            except ValueError:
                print('Введённые данные не являются координатами.')
                continue
            if self.pole[y][x]:
                self.pole[y][x].value = self.HUMAN_X
                self.free_cells -= 1
                self._compute_priority(y, x)
                break
            else:
                print('Выбранная клетка занята.')
                continue

    def computer_go(self):
        '''Ход компьютера'''
        free_cells = [(y, x) for y, row in enumerate(self.pole) for x, cell in enumerate(row) if cell]
        y, x = max(free_cells, key=lambda c: self.pole[c[0]][c[1]]._priority)
        if y == x == 1:  # Реакция на среднюю клетку
            for cell in (self.pole[0][1], self.pole[1][0], self.pole[1][2], self.pole[2][1]):
                cell._priority += 2
        self.free_cells -= 1
        self.pole[y][x].value = self.COMPUTER_O

    def _compute_priority(self, y, x):
        '''Просчёт хода компьютера'''
        # Реакция на ход противника
        for cell in self.pole[y]:
            cell._priority -= 1
        for cell in list(zip(*self.pole))[x]:
            cell._priority -= 1
        if y == x:
            for cell in self.diagonals[0]:
                cell._priority -= 1
        if y + x == 2:
            for cell in self.diagonals[1]:
                cell._priority -= 1
        # Корректировка опасности
        for row in self.pole + [list(lst) for lst in zip(*self.pole)] + self.diagonals:
            counter = [0, 0, 0]
            for cell in row:
                counter[cell.value] += 1
            if counter[1] == 2:
                for cell in row:
                    cell._priority = 5
            if counter[2] == 2:
                for cell in row:
                    cell._priority = 6

    def show(self):
        '''Отрисовка поля'''
        for row in self.pole:
            for cell in row:
                print(cell, end=' ')
            print()
        print('* ' * 10)


class Cell:
    def __init__(self):
        self.value = 0
        self._priority = 2

    def __bool__(self):
        return not self.value

    def __str__(self):
        if self.value == 1:
            return 'X'
        if self.value == 2:
            return '0'
        return '-'

    def __eq__(self, other):
        return self.value == other.value

    def __hash__(self):
        return hash(self.value)


if __name__ == '__main__':
    game = TicTacToe()
    game.init()
    step_game = 0
    while game:
        game.show()

        if step_game % 2 == 0:
            game.human_go()
        else:
            game.computer_go()

        step_game += 1

    game.show()

    if game.is_human_win:
        print("Поздравляем! Вы победили!")
    elif game.is_computer_win:
        print("Все получится, со временем")
    else:
        print("Ничья.")
