import random
from operator import mul
from pprint import pprint
cimport cython

cdef class CMatrix:
    #cdef float[:,:] data
    #cdef float[:,:] transposed
    cdef public int m
    cdef public int n
    cdef dict __dict__
    def __cinit__(self, data):
        # print(data)
        super().__init__()
        self.data = data
        self.m = len(data)

        cdef int first_len = len(data[0])
        cdef int i, j
        for i in range(self.m):
            if len(data[i]) != first_len:
                raise ArithmeticError("Разные длины строк в матрице") 
        self.n = first_len

        #if all([len(row) == len(data[0]) for row in data]):
        #    self.n = len(data[0])
        #else:
        #    raise ArithmeticError("Разные длины строк в матрице")

        self.transposed = []
        for i in range(self.m):
            local_row = []
            for j in range(self.n):
                local_row.append(data[j][i])
            self.transposed.append(local_row)
        #self.transposed = [[self.data[j][i] for j in range(len(self.data))] for i in range(len(self.data[0]))]

    cpdef void _transpose(self):
        self.transposed, self.data = self.data, self.transposed

    cpdef void _pure_calculate_transpose(self):
        cdef int i, j
        self.transposed = []
        for i in range(self.m):
            local_row = []
            for j in range(self.n):
                local_row.append(self.data[j][i])
            self.transposed.append(local_row)
        # self.transposed = [[self.data[j][i] for j in range(len(self.data))] for i in range(len(self.data[0]))]

    def T(self):
        return self.transposed

    def __add__(self, other):
        """Метод сложения двух объектов"""
        cdef int i, j
        if type(self) == CMatrix and type(other) == CMatrix:
            # return CMatrix([[self_elem + other_elem for self_elem, other_elem in zip(row_self, row_other)] for row_self, row_other in zip(self.data, other.data)])
            new_list = []
            for i in range(self.m):
                local_row = []
                for j in range(self.n):
                    local_row.append(self.data[i][j] + other.data[i][j])
                new_list.append(local_row)
            return CMatrix(new_list)
            
        elif any([isinstance(self, (int, float)), isinstance(other, (int, float))]):
            const = self if isinstance(self, (int, float)) else other
            if const == other:
                matrix = self
            elif const == self:
                matrix = other
            new_list = []
            for i in range(matrix.m):
                local_row = []
                for j in range(matrix.n):
                    local_row.append(matrix[(i,j)] + const)
                new_list.append(local_row)
            return CMatrix(new_list)
            # return CMatrix([[const + elem for elem in row] for row in self.data])
        

    def __iadd__(self, other):
        self = self + other
        return self

    def __sub__(self, other):
        cdef int i, j
        if type(self) == CMatrix and type(other) == CMatrix:
            new_list = []
            for i in range(self.m):
                local_row = []
                for j in range(self.n):
                    local_row.append(self.data[i][j] - other.data[i][j])
                new_list.append(local_row)
            return CMatrix(new_list)     
            # return CMatrix([[self_elem - other_elem for self_elem, other_elem in zip(row_self, row_other)] for row_self, row_other in zip(self.data, other.data)])
        elif any([isinstance(self, (int, float)), isinstance(other, (int, float))]):
            const = self if isinstance(self, (int, float)) else other
            if const == other:
                matrix = self
            elif const == self:
                matrix = other
            new_list = []
            for i in range(matrix.m):
                local_row = []
                for j in range(matrix.n):
                    if const == self:
                        local_row.append(const - matrix[(i, j)])
                    elif const == other:
                        local_row.append(matrix[(i,j)] - const)
                new_list.append(local_row)
            return CMatrix(new_list)
            # return CMatrix([[const - elem for elem in row] for row in self.data])

    def __isub__(self, other):
        self = self - other
        return self

    def __mul__(self, other):
        cdef int i, j, k
        if type(self) == CMatrix and type(other) == CMatrix:
            if self.m != other.n:
                raise ArithmeticError("Количество строк первой матрицы не совпадает с количеством столбцов второй")
            new_list = []
            for i in range(self.m):
                local_row = []
                for j in range(other.n):
                    row_sum = 0
                    for k in range(self.n):
                        row_sum += self.data[i][k] * other.data[k][j]
                    local_row.append(row_sum)
                new_list.append(local_row)
            return CMatrix(new_list)
            
            # return CMatrix([[sum(map(lambda x, y: x * y, row, column)) for column in other.transposed] for row in self.data])
        elif any([isinstance(self, (int, float)), isinstance(other, (int, float))]):
            const = self if isinstance(self, (int, float)) else other
            if const == other:
                matrix = self
            elif const == self:
                matrix = other
            new_list = []
            for i in range(matrix.m):
                local_row = []
                for j in range(matrix.n):
                    local_row.append(matrix[(i,j)] * const)
                new_list.append(local_row)
            return CMatrix(new_list)
            # return CMatrix([[const * elem for elem in row] for row in self.data])

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
    A = CMatrix([[1,5,2], [3,6,8], [9,7,4]])
    B = CMatrix([[4,7,8], [9,3,1], [2,5,6]])
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

    A1 = CMatrix([[random.randint(-1000,1000) for _ in range(n1)] for _ in range(m1)])
    B1 = CMatrix([[random.randint(-1000,1000) for _ in range(n1)] for _ in range(m1)])
    pprint(A1)
    pprint(B1)
    pprint(A1 + B1)

    A2 = CMatrix([[random.randint(-1000,1000) for _ in range(n1)] for _ in range(m1)])
    B2 = CMatrix([[random.randint(-1000,1000) for _ in range(m1)] for _ in range(n1)])
    pprint(A2 * B2)

