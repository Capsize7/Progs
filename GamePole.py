from random import randint, choice

ANS_FOR_CHOICE_MODE = '''Для продолжения необходимо выбрать режим игры.
Для того, чтобы выбрать классический режим введите "1".
Для выбора режима с движущимися кораблями введите "2".
Для вызова справки по игровым режимам введите "help"\n'''

ANS_FOR_CHOICE_POLE_SIZE = '''Для продолжения необходимо ввести размер поля
(одно целое число в диапозоне от 7 до 11 включительно): '''

HELP = '''---------------------------СПРАВКА---------------------------
В классическом режиме корабли не перемещаются по игровому полю.
В режиме с движущимися кораблями неподбитые корабли перемещаются после каждого хода.
Поэтому в классическом режиме при выстреле в ту клетку противника,
по которой вы ранее не стреляли, если в этой клетке нет
вражеского корабля, она изменит свою иконку с ⬛️ на 🌊.
В режиме с движущимися кораблями этого не будет происходить,
и черный квадрат так им и останется так как, повторюсь,
неподбитые корабли двигаются после каждого хода. Более подробно
о выбранном вами режиме будет рассказано после его выбора
непосредственно перед началом игры.
-------------------------------------------------------------'''

TITLE = '=' * 30 + 'МОРСКОЙ БОЙ' + '=' * 30

START_RULES = '''Ниже показано отображение игрового поля. Слева распологается поле
противника, справа ваше поле.'''

RULES_FOR_CLASSIC = '''Корабли распологаются в случайном порядке как у вас, так и у противника.
Расположение короблей противника вы не видите, поэтому на поле противника одни черные квадраты.
В любую черную клетку на поле противника можно выстрелить. Если в ней не оказалось
корабля, то клетка изменится с ⬛ на 🌊. Если окажется корабль то иконка сменится
на 🔥, если вы подбили корабль и у него остались еще палубы, а если
у корабля не осталось палуб то иконка ⬛ поменяется на 💀.

Кратко пробежимся по всем иконкам, которые используются при отображении игрового поля:
⬛️ - так отображаются те клетки противника, по которым можно выстрелить; 
🌊 - на вашем игровом поле так отображаются клетки, в которых нет корабля.
В поле противника так отображаются те клетки, по которым вы ранее стреляли
но корабля там не оказалось;
🔥 - так отображается подбитая палуба корабля, как на вашемполе, так
и на поле противника;
💀 - так отображается корабль, у которого все палубы подбиты, как на вашем
поле, так и на поле противника.

Для того, чтобы сделать ход необходимо вести через пробел два числа
в диапозоне от 0 до размера поля не включительно (размер поля вы вводили чуть ранее).
Первая цифра - это столбец выбранной вами клетки, вторая - строка.
Вы ходите первыми. Удачи!'''

RULES_FOR_MOVED = '''Корабли распологаются в случайном порядке как у вас, так и у противника.
Расположение короблей противника вы не видите, поэтому на поле противника одни черные квадраты.
Более того - если вы сделали ход и в той клетке, которую вы указали не оказалось корабля противника,
то данная клетка также останется черной, по причине того, что после каждого хода что ваши не подбитые корабли,
что не подбитые коробли противника будут перемещаться.
Изменятся на поле противника будут после попадания только те клетки, в которых был корабль, так как
подбитые корабли не перемещаются.

При отображении игрового поля используются следующие иконки:
⬛️ - так отображаются те клетки противника, по которым можно выстрелить; 
🌊 - на вашем игровом поле так отображаются клетки, в которых нет корабля.
В поле противника не будет таких иконок;
🔥 - так отображается подбитая палуба корабля, как на вашем
поле, так и на поле противника;
💀 - так отображается корабль, у которого все палубы подбиты, как
на вашем поле, так и на поле противника.
'''

END_RULES = '''Для того, чтобы сделать ход необходимо ввести через пробел два числа
в диапозоне от 0 до размера поля не включительно (размер поля вы вводили чуть ранее).
Первая цифра - это столбец выбранной вами клетки, вторая - строка.
Вы ходите первыми. Удачи!'''

UNDER_LINE = '=' * 71


class SizeRangeException(Exception):
    '''Данное исключение возникает тогда, когда пользователь
    вводит целое число n, которое не находится в диапозоне 7 <= n <= 10.
    Нужен для отладки ввода размеров поля, а также координат клеток в игре'''


class DescriptorForShip:

    def __set_name__(self, owner, name):
        self.name = '_' + name

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value


class Ship:
    tp = DescriptorForShip()
    length = DescriptorForShip()
    is_move = DescriptorForShip()

    def __init__(self, length, tp=1, x=None, y=None):
        self._x, self._y = x, y
        self._length = length
        self._tp = tp
        self._is_move = True
        self._cells = [1] * length
        self._is_dead = False

    def __getitem__(self, indx):
        '''Данный метод должен возвращать значение коллекции _cells корабля по переданому индексу'''
        return self._cells[indx]

    def __setitem__(self, indx, value):
        '''При помощи данного метода нужно подстреливать части корабля'''
        if not self._is_dead:
            if value == 2:
                self._is_move = False
                self._cells[indx] = value
            if {*self._cells} == {2}:
                self._is_dead = True
                self._cells[:] = [3] * self._length

    @property
    def is_dead(self):
        return self._is_dead

    def set_start_coords(self, x, y):
        '''Данный метод устанавливает координаты начала корабля'''
        self._x, self._y = x, y

    def get_start_coords(self):
        '''Данный метод возвращает кортеж с кораблями'''
        return self._x, self._y

    def move(self, go):
        '''данный метод должен перемещать корабль на одну клетку либо вперед, либо назад
        в направлении своей ориентации если флаг _is_move равен True'''
        if self._tp == 1:
            self._x += go
        else:
            self._y += go

    def is_collide(self, ship):
        '''Данный метод должен возвращать True если возможно столкновение с кораблем ship
        и False в противном случае'''
        if self._tp == 1:
            if ship._tp == 1:
                check1 = self._x - 1 <= ship._x <= self._x + self._length
                check2 = self._x - 1 <= ship._x + ship._length - 1 <= self._x + self._length
                check3 = self._y - 1 <= ship._y <= self._y + 1
            else:  # ship._tp == 2
                check1 = self._y - 1 <= ship._y <= self._y + 1
                check2 = self._y - 1 <= ship._y + ship._length - 1 <= self._y + 1
                check3 = self._x - 1 <= ship._x <= self._x + self._length
        else:  # self._tp == 2
            if ship._tp == 1:
                check1 = self._x - 1 <= ship._x <= self._x + 1
                check2 = self._x - 1 <= ship._x + ship._length - 1 <= self._x + 1
                check3 = self._y - 1 <= ship._y <= self._y + self._length
            else:  # ship._tp == 2
                check1 = self._y - 1 <= ship._y <= self._y + self._length
                check2 = self._y - 1 <= ship._y + ship._length - 1 <= self._y + self._length
                check3 = self._x - 1 <= ship._x <= self._x + 1
        return (check1 or check2) and check3

    def is_out_pole(self, size):
        '''Данный метод должен проверять на то, выходит ли корабль за пределы игрового поля и возвращать True
        если вышел и False в противном случае'''
        if self._tp == 1:
            return self._x < 0 or self._x + self._length > size
        return self._y < 0 or self._y + self._length > size

    def set_shot(self, x, y):
        '''Данный метод возвращает True, если коралль подстрелили,
        а таже непосредственно подстреливает кораль'''
        if self._tp == 1:
            if self._y == y and self._x <= x < self._x + self._length:
                self.__setitem__(x - self._x, 2)
                return True
            return False
        else:
            if self._x == x and self._y <= y < self._y + self._length:
                self.__setitem__(y - self._y, 2)
                return True
            return False


class GamePole:

    def __init__(self, size):
        self._size = size
        self._ships = list()

    def init(self):
        '''Данный метод инициализирует игру. Создает коробли и расставляет их на игровом поле.

        Проблему зависания при поиске места для последних короблей решил достаточно в лоб и топорно
        но тем не менее способ рабочий) Если за 100 попыток не удалось найти место для коробля, то просто
        рекурсивно вызываю init и все начинаю с начала. Для поля 7 x 7 в среднем за 5-10 рекурсивных вызовов
        формирует поле. Вечных зависаний не наблюдал при тех же 7)'''
        for length in range(4, 0, -1):
            for _ in range(5 - length):
                try_count = 0
                while True:
                    try_count += 1
                    if try_count == 100:
                        self._ships.clear()
                        self.init()
                        return
                    ship = Ship(length, randint(1, 2), randint(0, self._size - 1), randint(0, self._size - 1))
                    if ship.is_out_pole(self._size):
                        continue
                    if self.__checking_collisions_with_other_ships(ship):
                        self._ships.append(ship)
                        break

    def __checking_collisions_with_other_ships(self, check_ship):
        '''Данный метод проверяет соприкасается ли корабль с другими караблями и
        возвращает False если соприкасается, а True в противном случае'''
        for ship in self._ships:
            if check_ship is not ship and check_ship.is_collide(ship):
                return False
        return True

    def get_ships(self):
        '''Возвращает список кораблей'''
        return self._ships

    def move_ships(self):
        '''Если корабль не подбит и его возможно переместить на одну клетку без
        столкновения с другими кораблями то метод переместит корабль.
        Также данный метод меняет ориентацию
        однопалубного корабля если
        не удалась попытка его перемещения
        с базовой ориентацией'''

        def move_ship_procedure():
            '''Вспомогательная функция которая непосредственно двигает корабль'''
            shift = choice((-1, 1))
            ship.move(shift)
            if check_for_move_ship_prod():
                ship.move(-shift * 2)
                if check_for_move_ship_prod():
                    ship.move(shift)
                    return False
            return True

        def check_for_move_ship_prod():
            '''Функция проверяет можно ли подвигуть корабль'''
            return ship.is_out_pole(self._size) \
                or not self.__checking_collisions_with_other_ships(ship)

        for ship in self._ships:
            if ship.is_move:
                if ship.length == 1:
                    if not move_ship_procedure():
                        ship.tp = 1 if ship.tp == 2 else 2
                        move_ship_procedure()
                else:
                    move_ship_procedure()

    def get_pole(self):
        '''Возвращает вложенный список, в котором отображается игровое поле.
        0 - вода
        1 - корабль или часть корабля
        2 - подбитый корабль или часть корабля'''
        pole = [[0] * self._size for _ in range(self._size)]
        for ship in self._ships:
            x, y = ship.get_start_coords()
            for shift in range(ship.length):
                if ship.tp == 1:
                    pole[y][x + shift] = ship[shift]
                else:
                    pole[y + shift][x] = ship[shift]
        return tuple(map(tuple, pole))

    def show(self):
        '''Выводит в консоль игровое поле
        0 - вода
        1 - корабль или часть корабля
        2 - подбитый корабль или часть корабля'''
        pole = self.get_pole()
        for line in pole:
            print(' '.join(map(str, line)))


class PlayerSeaBattle:
    '''Родительский класс для классов игрока и компьютера'''

    def __init__(self, game_obj):
        self.pole = GamePole(game_obj.pole_size)
        self.pole.init()
        self._pole_size = game_obj.pole_size
        self._game_obj = game_obj
        # В shot_cells список попадают те координаты клеток, после стрельбы в которые были уже попадания
        self._shoot_cells = list()
        # Количество подбитых вражеских кораблей. Нужно для завершения игры и определения победителя
        self.count_opponent_dead_ship = 0

    def step(self):
        '''Реализует логику взаимодействия пользователя с игровым полем компьютерного противника.
        Примерно одинаково определен в каждом из дочерних классов со своими небольшими особенностями'''
        raise NotImplementedError(f'Необходимо определить метод step в {self.__class__.__name__}')

    def _get_coords_for_shot(self):
        '''Данный метод реализует безопасный ввод координат пользователем.
        Примерно одинаково определен в каждом из дочерних классов со своими небольшими особенностями'''
        raise NotImplementedError(f'Необходимо определить метод _get_coords_for_shot в {self.__class__.__name__}')


class User(PlayerSeaBattle):
    '''Родительский класс, от которого будут наследоваться те классы, которые будут ответственны
    за логику самого игрока для классического морского боя, а также для мороского боя с движущимися кораблями'''

    def step(self, enemy_ships):
        '''Описание метода есть в родительском классе'''
        while self.count_opponent_dead_ship != 10:
            coords = self._get_coords_for_shot()
            ship = self._search_ship_for_shot(*coords, enemy_ships)
            if not ship:
                print('\n❌Вы промахнулись')
                print('-' * 40)
                break
            if not ship.is_dead:
                print('\n🔥Вы подбили корабль')
            else:
                self.count_opponent_dead_ship += 1
                print('\n💀Вы полностью уничтожили корабль')
            self._game_obj.show_game()

    def _get_coords_for_shot(self):
        '''Описание метода есть в родительском классе'''
        while True:
            coords = input('\nВведите координаты клетки (два числа через пробел): ')
            try:
                x, y = map(int, coords.split(' '))
                if not 0 <= x < self._pole_size \
                        or not 0 <= y < self._pole_size:
                    raise SizeRangeException
                if (x, y) in self._shoot_cells:
                    print('Вы уже выбирали данные координаты. Повторите ввод')
                    continue
            except ValueError:
                print(f"Вы ввели некорректные данные.\nНеобходимо ввести два числа через пробел.")
            except SizeRangeException:
                print(
                    f"Вы ввели некорректные данные.\nОба числа должны быть целыми и в диапазоне от 0 до {self._pole_size - 1}.")
            else:
                return x, y

    def _search_ship_for_shot(self, x, y, enemy_ships):
        '''Возвращает True если по введенным пользователям координатам располагался
        корабль у противника, а также непосредственно наносит удар по кораблю. Примерно
        одинаково определен в каждом из дочерних классов со своими небольшими особенностями'''
        raise NotImplementedError(f'Необходимо определить метод _search_ship_for_shot в {self.__class__.__name__}')


class UserForClassic(User):
    '''Данный класс реализует логику взаимодействия игрока с игрой в классическом режиме игры'''

    def _search_ship_for_shot(self, x, y, enemy_ships):
        '''Описание метода есть в родительском классе'''
        self._shoot_cells.append((x, y))
        for ship in enemy_ships:
            if ship.set_shot(x, y):
                return ship
        return False


class UserForMoveShips(User):
    '''Данный класс реализует логику взаимодействия игрока с игрой в режиме с движущимися кораблями'''

    def _search_ship_for_shot(self, x, y, enemy_ships):
        '''Описание метода есть в родительском классе'''
        for ship in enemy_ships:
            if ship.set_shot(x, y):
                self._shoot_cells.append((x, y))
                return ship
        return False


class Computer(PlayerSeaBattle):
    '''Родительский класс, от которого будут наследоваться те классы, которые будут ответственны
        за логику компьютерного противника игрока для классического морского боя, а также
        для мороского боя с движущимися кораблями'''

    def __init__(self, game_obj):
        super().__init__(game_obj)
        # curr_ship_shot_cells - список с координатами подбитых клеток текущего корабля. Очищается после каждого убитого корабля
        self._curr_ship_shot_cells = list()
        # В targets попадают координаты клеток, в которых должно быть продолжение коробля игрока
        self._targets = list()
        # map_user_dead_ships - это поле с убитыми вражескими кораблями. Нужно для того, чтобы компьютер не стрелял в те клетки, где очевидно не может быть коробля игрока. Обновляется каждый раз после убийства компьютером корабля игрока
        self._map_user_dead_ships = [[0] * self._pole_size for _ in range(self._pole_size)]
        # shoot_counter - это счетчик палуб корабля, который находится под атакой
        self._shoot_counter = 0
        # target_ship_is_dead == True если корабль, который находится под атакой еще не убит, но координаты на него уже есть
        self._target_ship_is_dead = False
        # tp_attacked_ship != None если мы определили ориентацию 3, 4 палубного корабляи принимает значение либо 1, либо 2 в зависимости от ориентации. Во всех остальных случаях == None
        self._tp_attacked_ship = None

    def _get_coords_for_shot(self):
        '''Метод возвращает координату для выстрела компьютера. Примерно одинаково
        определен в каждом из дочерних классов со своими небольшими особенностями'''
        raise NotImplementedError(f'Необходимо определить метод _get_coords_for_shot в {self.__class__.__name__}')

    def _check_coords_for_target(self, x, y):
        '''Данный метод проверяет коодинаты, которые сгенерировались
        для дальнейшего обстрела корабей. Проверяет, чтобы координаты не выходили за пределы
        карты, а проверяет чтобы координаты не были рядом с ранее убитыми кораблями.
        Примерно одинаково определен в каждом из дочерних классов со своими небольшими особенностями'''
        raise NotImplementedError(f'Необходимо определить метод _search_ship_for_shot в {self.__class__.__name__}')

    def _search_ship_for_shot(self, x, y, enemy_ships):
        '''Возвращает True если по выбранным компьютером координатам есть корабль игрока. Если корабль есть
        еще его непосредственно подстреливает.Примерно одинаково определен в каждом
        из дочерних классов со своими небольшими особенностями'''
        raise NotImplementedError(f'Необходимо определить метод _search_ship_for_shot в {self.__class__.__name__}')

    def _is_not_enemies_ships_around_coords(self, x, y):
        '''Данный метод возвращает True если вокруг координат НЕТ вражеских УБИТЫХ кораблей и
        False в противном случае. Нужен для того, чтобы не палить по тем клеткам, в которых
        точно не может быть корабля у игрока'''
        avoid_neg_coord = lambda coord: 0 if coord < 0 else coord
        return not bool(sum(sum(line[avoid_neg_coord(x - 1): x + 2])
                            for line in self._map_user_dead_ships[avoid_neg_coord(y - 1): y + 2]))

    def _upd_map_user_dead_ships(self, ship):
        '''Данный метод обновляет карту мертвых кораблей каждый раз, после убийства компьютером корабля'''
        x, y = ship.get_start_coords()
        for add in range(ship.length):
            if ship.tp == 1:
                self._map_user_dead_ships[y][x + add] = 1
            else:
                self._map_user_dead_ships[y + add][x] = 1

    # ---МЕТОДЫ ДЛЯ ЛОГИКИ РАБОТЫ МЕТОДА STEP---------------------------------------------
    def _set_targets_for_second_cell(self, x, y):
        '''Данный метод устанавливает координаты для обстрела второй клетки корабля'''
        for x, y in ((x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)):
            if self._check_coords_for_target(x, y):
                self._targets.append((x, y))

    def _set_targets_for_third_cell(self):
        '''Данный метод устанавливает координаты для обстела третьей палубы корабля.
        Также определяет ориаентацию коробля, который находится под атакой.
        Далее определяет "Предрешенность корабля". Предрешенным корабль считается
        тот, у которого количество дальнейших координат меньше либо равняется двум.
        Иначе придется гадать'''
        min_x, max_x = sorted(x for x, _ in self._curr_ship_shot_cells)
        min_y, max_y = sorted(y for _, y in self._curr_ship_shot_cells)
        self._tp_attacked_ship = 1 if min_y == max_y else 2
        if self._tp_attacked_ship == 1:
            y = min_y
            temp_targets = [(min_x - 2, y), (min_x - 1, y), (max_x + 1, y), (max_x + 2, y)]
        else:
            x = min_x
            temp_targets = [(x, min_y - 2), (x, min_y - 1), (x, max_y + 1), (x, max_y + 2)]
        self._targets.clear()
        for x, y in temp_targets:
            if self._check_coords_for_target(x, y):
                self._targets.append((x, y))
        if len(self._targets) <= 2:
            self._target_ship_is_dead = True
        else:
            x, y = min(self._curr_ship_shot_cells)
            if self._tp_attacked_ship == 1:
                self._targets[:] = [(x - 1, y)]
            else:
                self._targets[:] = [(x, y - 1)]

    def _set_targets_for_four_cell(self):
        '''Данный метод устанавливает координаты для уничтожения
        4 палубы корабля. Логика простая. Если дошли сюда, значит четвертая клетка может быть
        как с с одного конца, так и с другого. Вот эти две координаты и устанавливаются'''
        if self._tp_attacked_ship == 1:
            y = self._curr_ship_shot_cells[-1][1]
            min_x, _, max_x = sorted(x for x, _ in self._curr_ship_shot_cells)
            self._targets[:] = [(min_x - 1, y), (max_x + 1, y)]
        else:
            x = self._curr_ship_shot_cells[-1][0]
            min_y, _, max_y = sorted(y for _, y in self._curr_ship_shot_cells)
            self._targets[:] = [(x, min_y - 1), (x, max_y + 1)]

    def _set_targets_after_miss(self):
        '''Данный метод устанавливает координату если после установки
        координаты для третьей клетки мы промахнулись.
        Просто устанавливается координата с двух противоположных концов'''
        if self._tp_attacked_ship == 1:
            y = self._curr_ship_shot_cells[-1][1]
            max_x = max(self._curr_ship_shot_cells)[0]
            self._targets[:] = [(max_x + 1, y), (max_x + 2, y)]
        else:
            x = self._curr_ship_shot_cells[-1][0]
            max_y = max(self._curr_ship_shot_cells)[1]
            self._targets[:] = [(x, max_y + 1), (x, max_y + 2)]

    # -----------------------------------------------------------------------------------

    def step(self, enemy_ships):
        '''Основной метод который заведует логикой уничтожения короблей игрока'''
        log_actions = list()
        while self.count_opponent_dead_ship != 10:
            x, y = self._get_coords_for_shot()
            ship = self._search_ship_for_shot(x, y, enemy_ships)
            if ship:  # Если компьютер не промахнулся
                if not ship.is_dead:  # Если подстреленный корабль не убит
                    if not self._target_ship_is_dead:  # Если координаты корабля не определены
                        if self._shoot_counter == 0:  # Если мы подстрелили корабль ВПЕРВЫЕ
                            self._shoot_counter += 1
                            self._set_targets_for_second_cell(x, y)
                        elif self._shoot_counter == 1:  # Если мы подстрелили корабль во ВТОРОЙ раз
                            self._set_targets_for_third_cell()
                            self._shoot_counter += 1
                        elif self._shoot_counter == 2:  # Если мы подстрелили корабль в ТРЕТИЙ РАЗ
                            self._shoot_counter += 1
                            self._set_targets_for_four_cell()
                            self._target_ship_is_dead = True
                    log_actions.append(f'🔥Ваш {ship.length}-палубник подбит')
                else:  # Подстреленный корабль убит
                    self.count_opponent_dead_ship += 1
                    self._upd_map_user_dead_ships(ship)
                    self._targets.clear()
                    self._curr_ship_shot_cells.clear()
                    self._target_ship_is_dead = False
                    self._tp_attacked_ship = None
                    self._shoot_counter = 0
                    log_actions.append(f'☠️Ваш {ship.length}-палубник полностью уничтожен')
            else:  # Компьютер промахнулся
                if self._shoot_counter == 2 and not self._target_ship_is_dead:  # Компьютер промахнулся после того, как не угадал с координатами
                    self._target_ship_is_dead = True
                    self._set_targets_after_miss()
                self._print_log_actions(log_actions)
                break
        else:  # Если мы вышли из цикла while из-за того, что игрок проиграл
            if log_actions:
                self._print_log_actions(log_actions)

    def _print_log_actions(self, log_actions):
        '''Данный метод печатает на экран лог действий
        компьютерного оппанента'''
        if not log_actions:
            print('❌Ваш противник промахнулся')
        else:
            print('\n'.join(log_actions))
        self._game_obj.show_game()


class ComputerForClassic(Computer):
    '''Данный класс нужен для реализации поведения компьютера в игре в классическом режиме'''

    def _get_coords_for_shot(self):
        '''Метод возвращает координату для выстрела компьютера'''
        if self._targets:
            return self._targets.pop(0)
        while True:
            coords = randint(0, self._pole_size - 1), randint(0, self._pole_size - 1)
            if coords not in self._shoot_cells and self._is_not_enemies_ships_around_coords(*coords):
                return coords

    def _search_ship_for_shot(self, x, y, enemy_ships):
        '''Описание метода есть в родительском классе'''
        self._shoot_cells.append((x, y))
        for ship in enemy_ships:
            if ship.set_shot(x, y):
                self._curr_ship_shot_cells.append((x, y))
                return ship
        return False

    def _check_coords_for_target(self, x, y):
        '''Данный метод проверяет коодинаты, которые сгенерировались
        для дальнейшего обстрела корабей. Проверяет, чтобы координаты не выходили за пределы
        карты, а проверяет чтобы координаты не были рядом с ранее убитыми кораблями'''
        if 0 <= x < self._pole_size:
            if 0 <= y < self._pole_size:
                if (x, y) not in self._shoot_cells and self._is_not_enemies_ships_around_coords(x, y):
                    return True
        return False


class ComputerForMoveShips(Computer):
    '''Данный класс нужен для реализации поведения компьютера в игре в режиме с движущимися кораблями'''

    def _get_coords_for_shot(self):
        '''Метод возвращает координату для выстрела компьютера'''
        if self._targets:
            return self._targets.pop(0)
        while True:
            coords = randint(0, self._pole_size - 1), randint(0, self._pole_size - 1)
            if coords not in self._shoot_cells and self._is_not_enemies_ships_around_coords(*coords):
                return coords

    def _search_ship_for_shot(self, x, y, enemy_ships):
        '''Описание метода есть в родительском классе'''
        for ship in enemy_ships:
            if ship.set_shot(x, y):
                self._shoot_cells.append((x, y))
                self._curr_ship_shot_cells.append((x, y))
                return ship
        return False

    def _check_coords_for_target(self, x, y):
        '''Данный метод проверяет коодинаты, которые сгенерировались
        для дальнейшего обстрела корабей. Проверяет, чтобы координаты не выходили за пределы
        карты, а проверяет чтобы координаты не были рядом с ранее убитыми кораблями'''
        if 0 <= x < self._pole_size:
            if 0 <= y < self._pole_size:
                if self._is_not_enemies_ships_around_coords(x, y):
                    return True
        return False


class SeaBattle:
    '''Данный класс является родительским для классов, экземпляры которых
    будут запускать игру'''

    def __init__(self):
        self._pole_size = self._set_pole_size()

    def _set_pole_size(self):
        '''Позволяет пользователю безопасно ввести размер поля'''
        while True:
            size = input(ANS_FOR_CHOICE_POLE_SIZE)
            try:
                size = int(size)
                if not 7 <= size <= 11:
                    raise SizeRangeException
            except ValueError:
                print("Вы ввели не целое число. Повторите ввод\n")
            except SizeRangeException:
                print(
                    "Вы ввели целое число, которое не находится в диапозоне от 7 до 11 включительно. Повторите ввод\n")
            else:
                return size

    @property
    def pole_size(self):
        return self._pole_size

    def _start_game(self):
        '''Данный метод печатает правила игры, а также запускает саму игру'''
        raise NotImplementedError(f'Необходимо определить метод _start_game в {self.__class__.__name__}')

    def _game(self):
        '''Данный метод ответственен за ход самой игры'''
        raise NotImplementedError(f'Необходимо определить метод _game в {self.__class__.__name__}')

    def show_game(self):
        '''Данный метод отображает игровое поля пользователя и компьюетрого противника'''
        raise NotImplementedError(f'Необходимо определить метод show_game в {self.__class__.__name__}')


class ClassicSeaBattle(SeaBattle):

    def __init__(self):
        super().__init__()
        self._user = UserForClassic(self)
        self._comp = ComputerForClassic(self)
        self._start_game()

    def _start_game(self):
        '''Описание метода есть в родительском классе'''
        print()
        print(TITLE)
        print(START_RULES)
        self.show_game()
        print(RULES_FOR_CLASSIC)
        print(END_RULES)
        print(UNDER_LINE)
        self._game()

    def _game(self):
        '''Описание метода есть в родительском классе'''
        game_step = 0
        while self._user.count_opponent_dead_ship != 10 and self._comp.count_opponent_dead_ship != 10:
            if not game_step % 2:
                self._user.step(self._comp.pole.get_ships())
            else:
                self._comp.step(self._user.pole.get_ships())
            game_step += 1
        if self._user.count_opponent_dead_ship == 10:
            print('Вы победили!')
        else:
            print('Вы проиграли...')

    def show_game(self):
        '''Описание метода есть в родительском классе'''
        player_pole = self._user.pole.get_pole()
        computer_pole = self._comp.pole.get_pole()
        player_chars = ['🌊', '🛳', '🔥', '💀️']
        comp_chars = ['⬛', '⬛', '🔥', '💀️']
        fields_chars = ['0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
        print()
        print('  ', end='')
        print(*fields_chars[:self._pole_size], sep='')
        for y in range(self._pole_size):
            print(fields_chars[y], end='')
            for x in range(self._pole_size):
                if computer_pole[y][x] == 0 and (x, y) in self._user._shoot_cells:
                    print('🌊', end='')
                else:
                    print(comp_chars[computer_pole[y][x]], end='')
            print('   ', end='')
            for cell in player_pole[y]:
                print(player_chars[cell], end='')
            print()
        print()


class MoveShipsSeaBattle(SeaBattle):

    def __init__(self):
        super().__init__()
        self._user = UserForMoveShips(self)
        self._comp = ComputerForMoveShips(self)
        self._start_game()

    def _start_game(self):
        '''Описание метода есть в родительском классе'''
        print()
        print(TITLE)
        print(START_RULES)
        self.show_game()
        print(RULES_FOR_MOVED)
        print(END_RULES)
        print(UNDER_LINE)
        self._game()

    def _game(self):
        '''Описание метода есть в родительском классе'''
        game_step = 0
        while self._user.count_opponent_dead_ship != 10 and self._comp.count_opponent_dead_ship != 10:
            if not game_step % 2:
                self._user.step(self._comp.pole.get_ships())
                self._comp.pole.move_ships()
            else:
                self._comp.step(self._user.pole.get_ships())
                self._user.pole.move_ships()
            game_step += 1
        if self._user.count_opponent_dead_ship == 10:
            print('Вы победили!')
        else:
            print('Вы проиграли...')

    def show_game(self):
        '''Описание метода есть в родительском классе'''
        player_pole = self._user.pole.get_pole()
        computer_pole = self._comp.pole.get_pole()
        player_chars = ['🌊', '🛳', '🔥', '💀️']
        comp_chars = ['⬛', '⬛', '🔥', '💀️']
        fields_chars = ['0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
        print()
        print('  ', end='')
        print(*fields_chars[:self._pole_size], sep='')
        for i in range(self._pole_size):
            print(fields_chars[i], end='')
            for cell in computer_pole[i]:
                print(comp_chars[cell], end='')
            print('   ', end='')
            for cell in player_pole[i]:
                print(player_chars[cell], end='')
            print()
        print()


def start_game():
    '''Для запуска игры необходимо вызвать эту функцию'''
    print('Добро пожаловать в МОРСКОЙ БОЙ!')
    while True:
        try:
            ans = input(ANS_FOR_CHOICE_MODE)
            if ans.lower().strip() == 'help':
                print(HELP)
                continue
            ans = int(ans)
            if ans not in (1, 2):
                raise ValueError
        except ValueError:
            print('Введены некорректные данные. Повторите ввод.\n')
        else:
            if ans == 1:
                ClassicSeaBattle()
            else:
                MoveShipsSeaBattle()
            ans = input('Чтобы сыграть еще раз введите "да": ')
            if ans.lower().strip() != 'да':
                break
            print()


if __name__ == '__main__':
    start_game()
