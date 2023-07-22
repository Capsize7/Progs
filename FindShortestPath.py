'''
Необходимо написать универсальную основу для представления ненаправленных связных графов и поиска в них кратчайших маршрутов.
Далее, этот алгоритм предполагается применять для прокладки маршрутов: на картах, в метро и так далее.
Vertex - для представления вершин графа (на карте это могут быть: здания, остановки, достопримечательности и т.п.);
Link - для описания связи между двумя произвольными вершинами графа (на карте: маршруты, время в пути и т.п.);
LinkedGraph - для представления связного графа в целом (карта целиком).
'''


class Vertex:
    def __init__(self):
        self._links = []

    @property
    def links(self):
        return self._links

    def get_link(self, v):
        '''Возвращает ребро с другим узлом, если есть'''
        for link in self._links:
            if link.get_v(self) is v:
                return link


class Link:
    def __init__(self, v1, v2, dist=1):
        self._v1 = v1
        self._v2 = v2
        self._dist = dist

    def __eq__(self, other):
        return (self._v1, self._v2) == (other.v1, other.v2) or (self._v1, self._v2) == (other.v2, other.v1)

    @property
    def v1(self):
        return self._v1

    @property
    def v2(self):
        return self._v2

    @property
    def dist(self):
        return self._dist

    @dist.setter
    def dist(self, value):
        self._dist = value

    def get_v(self, v):
        '''Возвращает второй узел'''
        return (self._v1, self._v2)[v is self.v1]


class LinkedGraph:
    def __init__(self):
        self._links = []
        self._vertex = []

    def add_vertex(self, v):
        '''Добавляет узел'''
        if v not in self._vertex:
            self._vertex.append(v)

    def add_link(self, link):
        '''Добавляет ребро'''
        if link not in self._links:
            self._links.append(link)
            for v in (link.v1, link.v2):
                self.add_vertex(v)
                v.links.append(link)

    def find_path(self, start_v, stop_v):
        '''Алгоритм Дейкстры'''
        costs = {link.get_v(start_v): link.dist for link in start_v.links}
        parents = dict.fromkeys(costs, start_v)
        processed = {start_v}

        def min_cost():
            return min(tuple(x for x in costs.items() if x[0] not in processed or x[0] == stop_v),
                       key=lambda x: x[1])[0]

        vertex = min_cost()
        while vertex != stop_v:
            cost = costs[vertex]
            for link in vertex.links:  # Перебираем все связи узла
                new_cost = cost + link.dist  # Стоимость с новой связью
                linked_vertex = link.get_v(vertex)  # Получаем узел по связи
                costs.setdefault(linked_vertex, new_cost)  # Добавляем стоимость до него, если нет
                parents.setdefault(linked_vertex, vertex)  # Добавляем его родителя, если нет
                if costs[linked_vertex] > new_cost:  # Если старая стоимость до узла больше
                    costs[linked_vertex] = new_cost  # Назначаем новую стоимость
                    parents[linked_vertex] = vertex  # Указываем нового родителя
            processed.add(vertex)  # Узел обработан
            vertex = min_cost()

        vertices = [stop_v]
        links = []
        while vertex != start_v:
            links.append(vertex.get_link(parents[vertex]))
            vertex = parents[vertex]
            vertices.append(vertex)
        vertices.reverse()
        links.reverse()
        return vertices, links


class Station(Vertex):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def __repr__(self):
        return self.name


class LinkMetro(Link):
    pass


if __name__ == '__main__':
    map2 = LinkedGraph()
    v1 = Vertex()
    v2 = Vertex()
    v3 = Vertex()
    v4 = Vertex()
    v5 = Vertex()

    map2.add_link(Link(v1, v2))
    map2.add_link(Link(v2, v3))
    map2.add_link(Link(v2, v4))
    map2.add_link(Link(v3, v4))
    map2.add_link(Link(v4, v5))

    assert len(map2._links) == 5, "неверное число связей в списке _links класса LinkedGraph"
    assert len(map2._vertex) == 5, "неверное число вершин в списке _vertex класса LinkedGraph"

    map2.add_link(Link(v2, v1))
    assert len(map2._links) == 5, "метод add_link() добавил связь Link(v2, v1), хотя уже имеется связь Link(v1, v2)"

    path = map2.find_path(v1, v5)
    s = sum([x.dist for x in path[1]])
    assert s == 3, "неверная суммарная длина маршрута, возможно, некорректно работает объект-свойство dist"

    assert issubclass(Station, Vertex) and issubclass(LinkMetro,
                                                      Link), "класс Station должен наследоваться от класса Vertex, а класс LinkMetro от класса Link"

    map2 = LinkedGraph()
    v1 = Station("1")
    v2 = Station("2")
    v3 = Station("3")
    v4 = Station("4")
    v5 = Station("5")

    map2.add_link(LinkMetro(v1, v2, 1))
    map2.add_link(LinkMetro(v2, v3, 2))
    map2.add_link(LinkMetro(v2, v4, 7))
    map2.add_link(LinkMetro(v3, v4, 3))
    map2.add_link(LinkMetro(v4, v5, 1))

    assert len(map2._links) == 5, "неверное число связей в списке _links класса LinkedGraph"
    assert len(map2._vertex) == 5, "неверное число вершин в списке _vertex класса LinkedGraph"

    path = map2.find_path(v1, v5)

    assert str(path[0]) == '[1, 2, 3, 4, 5]', path[0]
    s = sum([x.dist for x in path[1]])
    assert s == 7, "неверная суммарная длина маршрута для карты метро"
