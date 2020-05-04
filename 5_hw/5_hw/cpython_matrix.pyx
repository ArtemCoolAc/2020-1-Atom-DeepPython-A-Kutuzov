import random
from pprint import pprint
from operator import mul

cimport cython

cdef class Matrix:
    cdef int m
    cdef int n
    cdef dict __dict__
    def __cinit__(self, data):
        super().__init__()
        self.data = data
        self.m = len(data)
        if all([len(row) == len(data[0]) for row in data]):
            self.n = len(data[0])
        else:
            raise ArithmeticError("Разные длины строк в матрице")
        self.transposed = [[self.data[j][i] for j in range(len(self.data))] for i in range(len(self.data[0]))]

    cpdef void _transpose(self):
        self.transposed, self.data = self.data, self.transposed

    cpdef void _pure_calculate_transpose(self):
        self.transposed = [[self.data[j][i] for j in range(len(self.data))] for i in range(len(self.data[0]))]

    def T(self):
        return self.transposed

    def __add__(self, other):
        """Метод сложения двух объектов"""
        if type(self) == Matrix and type(other) == Matrix:
            return Matrix([[self_elem + other_elem for self_elem, other_elem in zip(row_self, row_other)] for row_self, row_other in zip(self.data, other.data)])
        elif any([isinstance(self, (int, float)), isinstance(other, (int, float))]):
            const = self if isinstance(self, (int, float)) else other
            matrix = other if const == self else self
            return Matrix([[const + elem for elem in row] for row in matrix.data])
        

    def __iadd__(self, other):
        self = self + other
        return self

    def __sub__(self, other):
        if type(self) == Matrix and type(other) == Matrix:      
            return Matrix([[self_elem - other_elem for self_elem, other_elem in zip(row_self, row_other)] for row_self, row_other in zip(self.data, other.data)])
        elif any([isinstance(self, (int, float)), isinstance(other, (int, float))]):
            const = self if isinstance(self, (int, float)) else other
            return Matrix([[const - elem for elem in row] for row in self.data])

    def __isub__(self, other):
        self = self - other
        return self

    def __mul__(self, other):
        print(f"self is {str(self)}, other is {str(other)}")
        if type(self) == Matrix and type(other) == Matrix:
            if len(self.data) != len(other.transposed):
                raise ArithmeticError("Количество строк первой матрицы не совпадает с количеством столбцов второй")
            return Matrix([[sum(map(lambda x, y: x * y, row, column)) for column in other.transposed] for row in self.data])
        elif any([isinstance(self, (int, float)), isinstance(other, (int, float))]):
            const = self if isinstance(self, (int, float)) else other
            matrix = other if const == self else self
            return Matrix([[const * elem for elem in row] for row in matrix.data])

    def __getitem__(self, key):
        cdef int x = key[0]
        cdef int y = key[1]
        if isinstance(key, tuple) and all([isinstance(elem, int) for elem in key]) and (0 <= x <= self.m) and (0 <= y <= self.n):
            return self.data[x][y]
        else:
            raise KeyError("Неправильное индексирование")

    def __setitem__(self, key, value):
        cdef int x = key[0]
        cdef int y = key[1]
        if isinstance(key, tuple) and all([isinstance(elem, int) for elem in key]) and (0 <= x <= self.m) and (0 <= y <= self.n):
            self.data[x][y] = value
        else:
            raise KeyError("Некорректное индексирование")

    def __repr__(self):
        return str(self.data)

    def __str__(self):
        return str(self.data)

if __name__ == "__main__":
    A = Matrix([[1,5,2], [3,6,8], [9,7,4]])
    B = Matrix([[4,7,8], [9,3,1], [2,5,6]])
    C = A + B
    D = A - B
    E = A * B
    F = A + 2
    G = B * 10
    print(C)
    print(D)
    print(E)
    print(F)
    print(G)
    print(G.T())

    m1 = random.randint(2,10)
    n1 = random.randint(2,10)

    A1 = Matrix([[random.randint(-1000,1000) for _ in range(n1)] for _ in range(m1)])
    B1 = Matrix([[random.randint(-1000,1000) for _ in range(n1)] for _ in range(m1)])
    pprint(A1)
    pprint(B1)
    pprint(A1 + B1)

    A2 = Matrix([[random.randint(-1000,1000) for _ in range(n1)] for _ in range(m1)])
    B2 = Matrix([[random.randint(-1000,1000) for _ in range(m1)] for _ in range(n1)])
    pprint(A2 * B2)

