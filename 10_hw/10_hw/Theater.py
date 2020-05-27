import re


class Theater:

    def __init__(self, path):
        super().__init__()
        self.matrix = []
        try:
            with open(path, 'r') as file:
                for line in file:
                    some_list = list(map(int, re.sub(pattern=r'\s+', repl=' ', string=line.strip()).split(' ')))
                    if not all(list(map(lambda x: x in [0, 1], some_list))):
                        raise TypeError('Некорректные числа в файле')
                    self.matrix.append(some_list)
        except Exception as e:
            print(f'Ошибка: {e}')


    def calculate_free_places(self):
        if hasattr(self, 'free_places'):
            return self.free_places
        self.free_places = 0
        for row in self.matrix:
            self.free_places += (len(row) - sum(row))
        return self.free_places

    def __getitem__(self, row, column):
        if not isinstance(row, int) or not isinstance(column, int):
            raise TypeError('Неверный тип индекса')
        elif row > len(self.matrix) or column > len(self.matrix[row]):
            raise IndexError('Выход за границы театра')
        else:
            return self.matrix[row][column]

    def free_or_busy(self, row, column):
        mapping = {0: 'Свободно', 1: 'Занято'}
        return f'{mapping[self.__getitem__(row,column)]}'

    def __str__(self):
        return str(self.matrix)


if __name__ == '__main__':
    try:
        A = Theater('test.txt')
        print(f'Свободных мест в театре {A.calculate_free_places()}')
        print(f'Место (5,8) {A.free_or_busy(4,7)}')

    except Exception as e:
        print(f'Ошибка: {e}')

    try:
        print(f'Место (100,2) {A.free_or_busy(99,1)}')
        
    except Exception as e:
        print(f'Ошибка: {e}')

    try:
        print(f'Место (2,50) {A.free_or_busy(1,49)}')
    
    except Exception as e:
        print(f'Ошибка: {e}')
