'''
Реализуйте декоратор @limiter для декорирования класса,
 с помощью которого можно ограничивать количество создаваемых декорируемым классом экземпляров до определенного числа
'''

def limiter(limit, unique, lookup):
    instances = {}
    lookups = {}

    def wrapper(cls):
        def get_instance(*args, **kwargs):
            instance = cls(*args, **kwargs)
            lookups.setdefault('FIRST', instance)
            identifier = getattr(instance, unique)
            if len(instances) < limit:
                if identifier not in instances:
                    lookups['LAST'] = instances[identifier] = instance
                return instances[identifier]
            return instances.get(identifier) or lookups.get(lookup)

        return get_instance

    return wrapper

if __name__ == '__main__':
    @limiter(3, 'ID', 'LAST')
    class MyClass:
        def __init__(self, ID, value):
            self.ID = ID
            self.value = value


    obj1 = MyClass(1, 5)  # создается экземпляр класса с идентификатором 1
    obj2 = MyClass(2, 8)  # создается экземпляр класса с идентификатором 2
    obj3 = MyClass(3, 10)  # создается экземпляр класса с идентификатором 3

    obj4 = MyClass(4, 0)  # превышено ограничение limit, возвращается последний созданный экземпляр
    obj5 = MyClass(2, 20)  # возвращается obj2, так как экземпляр с идентификатором 2 уже есть

    print(obj4.value)
    print(obj5.value)