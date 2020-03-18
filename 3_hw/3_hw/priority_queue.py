import heapq
from typing import List
import unittest
import random
import copy


class PriorityQueue:
    def __init__(self):
        self.heap_list = [0]
        self.current_size = 0

    def perc_up(self, i):
        """Важнейший метод поддержания свойств кучи: если элемент меньше родителя, то меняем его с родителем местами"""
        while i // 2 > 0:
            if self.heap_list[i] < self.heap_list[i // 2]:  # если дитя меньше родителя
                self.heap_list[i // 2], self.heap_list[i] = self.heap_list[i], self.heap_list[i // 2]  # parent<->child
            i = i // 2

    def insert(self, k: int):
        """Вставка элемента: сначала просто вставляем в конец списка, но если свойства нарушаются,
        то продвигаем вставленного ребенка наверх"""
        self.heap_list.append(k)
        self.current_size += 1
        self.perc_up(self.current_size)

    def perc_down(self, i: int):
        """Операция прокидывания вниз нового корня "дерева" """
        while (i * 2) <= self.current_size:  # пока левый ребенок существует
            min_child = self.min_child(i)  # находим меньшего ребенка относительно i-го элемента
            if self.heap_list[i] > self.heap_list[min_child]:  # если i-ый элемент (родитель) больше ребенка, то обмен
                self.heap_list[i], self.heap_list[min_child] = self.heap_list[min_child], self.heap_list[i]
            i = min_child  # теперь i-ый элемент ребенок и пойдут проверки дальше, а можно ли ещё найти меньшего дитя

    def min_child(self, i: int):
        """Для восстановления свойств кучи после удаления корня возможна неоднократная операция прокидывания нового
        корня вниз, для этого необходимо найти позицию минимального ребенка"""
        if i * 2 + 1 > self.current_size:  # если правого ребенка просто нет, то возвращаем левого
            return i * 2
        else:
            if self.heap_list[i * 2] < self.heap_list[i * 2 + 1]:  # если левый ребенок меньше правого, то левого
                return i * 2
            else:  # иначе возвращаем правого
                return i * 2 + 1

    def del_min(self):
        """Метод удаления минимального элемента, это корень, удаляем его, на место корня становится 2-ой элемент и
         необходимо восстановить свойства кучи, делается это пробрасыванием его вниз"""
        min_value = self.heap_list[1]  # у нас куча [0, {root}, ..., ..., ... ]
        self.heap_list[1] = self.heap_list[self.current_size]
        self.current_size = self.current_size - 1
        self.heap_list.pop()
        self.perc_down(1)
        return min_value

    def heapify(self, some_list: List[int]):
        """Метод создания кучи из списка"""
        i = len(some_list) // 2
        self.current_size = len(some_list)
        self.heap_list = [0] + some_list
        while i > 0:
            self.perc_down(i)
            i -= 1
        return self.heap_list[1:]

    def heappop(self, some_list: List[int]):
        """Метод извлечения корневого элемента из кучи"""
        list2 = self.heapify(some_list)
        self.del_min()
        return self.heap_list[1:]

    def heappush(self, some_list: List[int], item: int):
        """Метод вставки элемента в кучу"""
        list2 = self.heapify(some_list)
        self.insert(item)
        return self.heap_list[1:]


class MyTestCase(unittest.TestCase):
    REPEATS_NUMBER = 100

    def test_my_heapify(self):
        for _ in range(self.REPEATS_NUMBER):
            length = random.randint(2, 100)
            some_list = [random.randint(-100, 100) for _ in range(length)]
            some_same_list = copy.deepcopy(some_list)
            B = PriorityQueue()
            heapq.heapify(some_list)
            some_same_list = B.heapify(some_same_list)
            self.assertEqual(some_list, some_same_list)

    def test_my_pop(self):
        for _ in range(self.REPEATS_NUMBER):
            length = random.randint(2, 100)
            some_list = [random.randint(-100, 100) for _ in range(length)]
            some_same_list = copy.deepcopy(some_list)
            A = PriorityQueue()
            heapq.heapify(some_list)
            heapq.heappop(some_list)
            some_same_list = A.heappop(some_same_list)
            self.assertEqual(some_same_list, some_list)

    def test_my_push(self):
        for _ in range(self.REPEATS_NUMBER):
            length = random.randint(2, 100)
            some_list = [random.randint(-100, 100) for _ in range(length)]
            some_same_list = copy.deepcopy(some_list)
            A = PriorityQueue()
            inserted = random.randint(-100, 100)
            heapq.heapify(some_list)
            heapq.heappush(some_list, inserted)
            some_same_list = A.heappush(some_same_list, inserted)
            self.assertEqual(some_same_list, some_list)




    # def __init__(self, raw_array=None):
    #     self.array = raw_array
    #
    # @staticmethod
    # def left(i):
    #     return 2 * i + 1
    #
    # @staticmethod
    # def right(i):
    #     return 2 * i + 2
    #
    # def max_heapify(self, i):
    #     largest = i
    #     n = len(self.array)
    #     left = self.left(i)
    #     right = self.right(i)
    #     if left < n and self.array[left] > self.array[largest]:
    #         largest = left
    #         # If right child is larger than largest so far
    #     if right < n and self.array[right] > self.array[largest]:
    #         largest = right
    #     # largest = self.array.index(max(self.array[i], self.array[left], self.array[right]))
    #     if largest != i:
    #         self.array[i], self.array[largest] = self.array[largest], self.array[i]
    #         self.max_heapify(largest)
    #
    # def heapify(self, some_list):
    #     self.array = some_list
    #     n = len(some_list)
    #     i = n // 2 - 1
    #     while i > 0:
    #         self.max_heapify(i)
    #         i -= 1

    # def heapify(self, arr, i):
    #     # self.array = arr
    #     n = len(arr)
    #     largest = i  # Initialize largest as root
    #     l = 2 * i + 1  # left = 2*i + 1
    #     r = 2 * i + 2  # right = 2*i + 2
    #
    #     # If left child is larger than root
    #     if l < n and arr[l] > arr[largest]:
    #         largest = l
    #
    #         # If right child is larger than largest so far
    #     if r < n and arr[r] > arr[largest]:
    #         largest = r
    #
    #         # If largest is not root
    #     if largest != i:
    #         arr[i], arr[largest] = arr[largest], arr[i]
    #         self.array = arr
    #         # Recursively heapify the affected sub-tree
    #         self.heapify(arr, largest)
    #
    # def build_heap(self, arr):
    #     i = len(arr) // 2 - 1
    #     for i in range(i, -1, -1):
    #         self.heapify(arr, i)


if __name__ == '__main__':
    a = [1, 8, 2, 4, 6, 9, 7]
    b = [1, 8, 2, 4, 6, 9, 7]
    A = PriorityQueue()
    d = A.heapify(a)
    c = PriorityQueue()
    heapq.heapify(b)
    print(b)
    print(d)
    a.pop()
    b.pop()
    heapq.heapify(a)
    g = A.heapify(b)
    print(a)
    print(g)

    aa = [-3, 16, -8, 2, -9]
    bb = [-3, 16, -8, 2, -9]

    heapq.heapify(aa)
    dd = A.heapify(bb)
    print(aa)
    print(dd)

    heapq.heappop(aa)
    A.del_min()
    ddd = A.heap_list[1:]
    print(aa)
    print(ddd)
    d = [1, 3, 5, 4, 6, 13, 10, 9, 8, 15, 17]
    e = [1, 3, 5, 4, 6, 13, 10, 9, 8, 15, 17]

    length = random.randint(2, 100)
    some_list = [random.randint(-100, 100) for _ in range(length)]
    some_same_list = copy.deepcopy(some_list)
    A = PriorityQueue()
    heapq.heapify(some_list)
    heapq.heappop(some_list)
    some_same_list2 = A.heappop(some_same_list)
    print(some_list)
    print(some_same_list2)


    unittest.main()

    # heapq.heapify(d)
    # print(d)
    # f = PriorityQueue()
    # f.heapify(e)
    # print(f.array)
