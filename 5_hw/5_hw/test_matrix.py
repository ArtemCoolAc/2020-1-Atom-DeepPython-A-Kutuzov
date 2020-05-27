import random
import time
from py_matrix import PyMatrix
from cpython_matrix import Matrix
from cython_matrix import CMatrix

def test_compare(m, n):
    some_list = [[random.randint(-1000,1000) for _ in range(n)] for _ in range(m)]
    another_list = [[random.randint(-1000,1000) for _ in range(n)] for _ in range(m)]
    A1 = PyMatrix(some_list)
    B1 = PyMatrix(another_list)
    A2 = Matrix(some_list)
    B2 = Matrix(another_list)
    A3 = CMatrix(some_list)
    B3 = CMatrix(another_list)
    time1 = time.time()
    C1 = A1 * B1
    time1f = time.time()
    time1 = time1f - time1
    time2 = time.time()
    C2 = A2 * B2
    time2f = time.time()
    time2 = time2f - time2
    time3 = time.time()
    C3 = A3 * B3
    time3f = time.time()
    time3 = time3f - time3
    print(f'Чистый питон - {time1}, полуСи-полуПитон - {time2}, близкий_С_варик - {time3}')
    return time1, time2, time3

some_list = [[random.randint(-1000,1000) for _ in range(1000)] for _ in range(1000)]
another_list = [[random.randint(-1000,1000) for _ in range(1000)] for _ in range(1000)]
ts1 = PyMatrix(some_list)
sa1 = PyMatrix(another_list)
ts2 = Matrix(some_list)
sa2 = Matrix(another_list)
ts3 = CMatrix(some_list)
sa3 = CMatrix(another_list)

def timer(f):
    def tmp(*args, **kwargs):
        t = time.time()
        res = f(*args, **kwargs)
        timef = time.time()-t       
        print(f'Время выполнения {f} равно {timef}')
        return res
    return tmp

@timer
def constructor1():
    A = PyMatrix(some_list)

@timer
def constructor2():
    A = Matrix(some_list)

@timer
def constructor3():
    A = CMatrix(some_list)

def check_constructors():
    constructor1()
    constructor2()
    constructor3()

@timer
def add1():
    C = ts1 + sa1

@timer
def add2():
    C = ts2 + sa2

@timer
def add3():
    C = ts3 + sa3

def check_add():
    add1()
    add2()
    add3()

if __name__ == '__main__':
    test_compare(100, 100)
    check_constructors()
    check_add()
