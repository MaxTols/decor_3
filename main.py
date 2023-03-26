import os

import types

from datetime import datetime


def logger(old_function):

    def new_function(*args, **kwargs):
        date = datetime.now()
        name_function = old_function.__name__
        result = old_function(*args, **kwargs)

        with open('homework.log', 'a') as file:
            file.write(f'Дата и время вызова функции - {date}\n' 
                       f'Название функции - {name_function}\n' 
                       f'Аргументы функции - {args}, {kwargs}\n' 
                       f'Значение функции - {result}\n\n')
        return result

    return new_function


def test_3():

    path = 'homework.log'
    if os.path.exists(path):
        os.remove(path)

    @logger
    def flat_generator(list_of_lists):
        for items in list_of_lists:
            for item in items:
                yield item

    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]

    for flat_iterator_item, check_item in zip(
            flat_generator(list_of_lists_1),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    ):
        assert flat_iterator_item == check_item

    assert list(flat_generator(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]

    assert isinstance(flat_generator(list_of_lists_1), types.GeneratorType)

    @logger
    class FlatIterator:

        def __init__(self, list_of_list):
            self.list_of_list = list_of_list
            self.count_1 = -1

        def __iter__(self):
            self.count_1 += 1
            self.count_2 = 0
            return self

        def __next__(self):
            if self.count_2 == len(self.list_of_list[self.count_1]):
                iter(self)
            if self.count_1 == len(self.list_of_list):
                raise StopIteration
            self.count_2 += 1
            return self.list_of_list[self.count_1][self.count_2-1]

    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]

    for flat_iterator_item, check_item in zip(
            FlatIterator(list_of_lists_1),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    ):

        assert flat_iterator_item == check_item

    assert list(FlatIterator(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]


if __name__ == '__main__':
    test_3()
