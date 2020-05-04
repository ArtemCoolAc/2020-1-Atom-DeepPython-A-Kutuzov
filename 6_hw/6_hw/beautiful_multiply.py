"""Модуль для вычисления произведения элементов списка без текущего
без использования операции деления"""

import math
import random
import logging

logging.basicConfig(filename='log.txt', level=logging.INFO)


def calculate_levels(some_list):
    n = math.ceil(math.log2(len(some_list)))  # вычисляем высоту дерева
    levels = [[*some_list]]  # начало дерева это сам список
    previous_level = [*some_list]  # предыдущий уровень сначала это сам список
    current_quantity = len(some_list)
    for _ in range(n):
        local_list = list()
        first_division = current_quantity >> 1  # количество элементов на уровень выше
        first_division = first_division if (not int(bin(current_quantity)[-1])) \
            else first_division + 1
        current_quantity = first_division
        # quan = math.ceil(len(some_list)/(2**(current_level+1)))
        prev_len = len(previous_level)  # значение длины предыдущего уровня
        for i in range(current_quantity):
            t1 = 2 * i;
            t2 = 2 * i + 1
            mult = previous_level[2 * i]  # берется нечетный элемент
            logging.debug(f"2i={t1},2i+1={t2},prev={previous_level}, mult={mult}, quan={prev_len}")
            if 2 * i + 1 < prev_len:  # проверка на наличие соседа
                mult *= previous_level[2 * i + 1]  # если сосед есть, то на него умножим
            local_list.append(mult)
        levels.append(local_list)  # добавляем новый уровень
        previous_level = levels[-1]  # предыдущий уровень для следующей итерации это текущий
    return levels


def get_pair(a, index):
    """Функция строит "дерево индексов" для полученного дерева"""
    cur_index = index
    indices = []
    for level in a:
        l = len(level)
        if cur_index % 2 == 0:  # если индекс четный
            if cur_index + 1 == l:  # если соседа нет
                first = None
            else:
                first = cur_index + 1  # берем правый элемент в качестве соседа
        else:  # если индекс нечетный
            first = cur_index - 1  # то берем левый элемент в качестве соседа
        cur_index >>= 1
        indices.append([first, cur_index])  # первый элемент - сосед, второй - корень
    return indices


def calculate_mul(some_list):
    """Главный метод подсчета произведения элементов списка, не включая текущего,
    причем без операции деления"""
    if not isinstance(some_list, list):
        raise TypeError("На вход может быть подан только список")
    elif not all(map(lambda x: isinstance(x, (int, float)), some_list)):
        raise ValueError("В списке могут быть только числа, никаких строк")
    elif len(some_list) == 0:
        raise ArithmeticError("Список не может быть пустым для данной")
    b = calculate_levels(some_list)  # строим дерево произведений над элементами
    new_list = list()
    for i in range(len(some_list)):
        index_tree = get_pair(b, i)  # строим дерево индексов для удобства дерева произведений
        logging.debug(f'index tree {index_tree}')
        level_up_mul = some_list[index_tree[0][0]] if index_tree[0][0] is not None else 1
        logging.info(f' {level_up_mul}')
        for j in range(1, len(b) - 1):  # проходим по нужной ветке и изменяем множитель
            level_up_mul = level_up_mul if index_tree[j][0] is None \
                else level_up_mul * b[j][index_tree[j][0]]
            logging.debug(f'Уровень {j}, прокидываем наверх {level_up_mul}')
        new_list.append(level_up_mul)
    return new_list


if __name__ == '__main__':
    for _ in range(10):
        A = calculate_mul([random.randint(1, 10) for _ in range(10)])
