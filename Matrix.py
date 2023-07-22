'''
Класс Matrix, описывающий двумерную матрицу
При передаче экземпляра класса Matrix в функцию round()
должен возвращаться новый экземпляр класса Matrix c исходным количеством строк и столбцов и с элементами,
округленными с помощью функции round().
Во время передачи в функцию round() должна быть возможность в качестве второго необязательного аргумента указать целое число,
определяющее количество знаков после запятой при округлении.
'''


class Matrix:
    def __init__(self, rows, cols, value=0):
        self.rows = rows
        self.cols = cols
        self.value = value
        self._matrix = [[value] * cols for _ in range(rows)]

    def get_value(self, row, col):
        return self._matrix[row][col]

    def set_value(self, row, col, value):
        self._matrix[row][col] = value

    def __str__(self):
        string_matrix = [[str(ele) for ele in row] for row in self._matrix]
        return '\n'.join(' '.join(row) for row in string_matrix)

    def __repr__(self):
        return f'Matrix({self.rows}, {self.cols})'

    def __pos__(self):
        matrix = Matrix(self.rows, self.cols)
        for row in range(matrix.rows):
            for col in range(matrix.cols):
                matrix.set_value(row, col, self.get_value(row, col))
        return matrix

    def __neg__(self):
        matrix = Matrix(self.rows, self.cols)
        for row in range(matrix.rows):
            for col in range(matrix.cols):
                matrix.set_value(row, col, -self.get_value(row, col))
        return matrix

    def __round__(self, n):
        matrix = Matrix(self.rows, self.cols)
        for row in range(matrix.rows):
            for col in range(matrix.cols):
                matrix.set_value(row, col, round(self.get_value(row, col), n))
        return matrix

    def __invert__(self):
        matrix = Matrix(self.cols, self.rows)
        for row in range(self.cols):
            for col in range(self.rows):
                matrix.set_value(row, col, self.get_value(col, row))
        return matrix


if __name__ == '__main__':
    matrix = Matrix(2, 3, 1)

    print(+matrix)
    print()
    print(-matrix)

    print('-' * 8)

    matrix = Matrix(2, 3, 1)

    print(matrix)
    print()
    print(~matrix)
