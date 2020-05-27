import heapq
from typing import List
import unittest
import random
import copy


class PriorityQueue:
    """Класс очередь с приоритетом - важная и интересная структура данных"""
    def __init__(self):
        self.heap_list = [0]
        self.current_size = 0

    def perc_up(self, i: int):
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
            length1 = random.randint(2, 100)
            some_list1 = [random.randint(-100, 100) for _ in range(length1)]
            some_same_list1 = copy.deepcopy(some_list1)
            b1 = PriorityQueue()
            heapq.heapify(some_list1)
            some_same_list1 = b1.heapify(some_same_list1)
            self.assertEqual(some_list1, some_same_list1)

    def test_my_pop(self):
        for _ in range(self.REPEATS_NUMBER):
            length2 = random.randint(3, 100)
            some_list22 = [random.randint(-100, 150) for _ in range(length2)]
            some_same_list22 = copy.deepcopy(some_list22)
            a1 = PriorityQueue()
            heapq.heapify(some_list22)
            heapq.heappop(some_list22)
            some_same_list22 = a1.heappop(some_same_list22)
            self.assertEqual(some_same_list22, some_list22)

    def test_my_push(self):
        for _ in range(self.REPEATS_NUMBER):
            length3 = random.randint(2, 100)
            some_list3 = [random.randint(-100, 100) for _ in range(length3)]
            some_same_list3 = copy.deepcopy(some_list3)
            a2 = PriorityQueue()
            inserted = random.randint(-100, 100)
            heapq.heapify(some_list3)
            heapq.heappush(some_list3, inserted)
            some_same_list3 = a2.heappush(some_same_list3, inserted)
            self.assertEqual(some_same_list3, some_list3)


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
