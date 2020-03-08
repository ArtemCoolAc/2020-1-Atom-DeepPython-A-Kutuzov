from itertools import zip_longest


class UserList(list):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def calculate_extra_length(len_self, len_other):
        """
        Статический метод подсчета максимальной длины, а также длин дополнения списков
        @param len_self: длина 1-го списока
        @param len_other: длина 2-го списка
        @return: возвращает максимальную длину, длину дополнени 1-го списка, 2-го списка (дополнение нулями)
        """
        max_length = len_self if len_self >= len_other else len_other
        extra_self_length = max_length - len_self if (max_length - len_self > 0) else 0
        extra_other_length = max_length - len_other if (max_length - len_other > 0) else 0
        return max_length, extra_self_length, extra_other_length

    def add(self, other):
        max_length, extra_self_length, extra_other_length = self.calculate_extra_length(len(self), len(other))
        self.extend([0] * extra_self_length)
        other.extend([0] * extra_other_length)
        return list(map((lambda x, y: x + y), self, other))

    def __add__(self, other):
        """
        Переопределение метода сложения списка (с конкатенации на поэлементное)
        @param other: 2-ой список
        @return: возвращает UserList после арифметичечкого сложения двух списков
        """
        return UserList([x + y for x, y in zip_longest(self, other, fillvalue=0)])

    def __iadd__(self, other):
        """
        Переопределение метода += списка (с конкатенации на поэлементное)
        @param other: 2-ой список
        @return: self'у присваивается сумма
        """
        self = self + other
        return self

    def __sub__(self, other):
        """
        Добавления оператора арифметического вычитания для списка
        @param other: 2-ой список
        @return: возвращает объект класса UserList как арифметическая разность двух списков
        """
        return UserList([x - y for x, y in zip_longest(self, other, fillvalue=0)])

    def __isub__(self, other):
        """
        Перегрузка оператора -= для списка
        @param other: 2-ой список
        @return: возвращает объект UserList после вычитания из исходного списка 2-го
        """
        self = self - other
        return self

    def __lt__(self, other):
        return sum(self) < sum(other)

    def __gt__(self, other):
        return sum(self) > sum(other)

    def __le__(self, other):
        return sum(self) <= sum(other)

    def __ge__(self, other):
        return sum(self) >= sum(other)

    def __eq__(self, other):
        return sum(self) == sum(other)

    def __ne__(self, other):
        return sum(self) != sum(other)


a = UserList([23, 35, 23])
c = [6, 7, 8]
d = a + c
print(f'Вот он d {d}')
d = d + a
print(f'Вот он d {d}')
a += [2, 5, 10, 1]
print(f'после сложения {a}')
b = [1, 5, 10, 20, 50, 100, 1000, 10000, 3434, 233]
a - b
a = a - b
print(f'после a = a - b {a}')
a -= [-100, -500, -1000, 500]
print(f'после a -=')
print(a)

aa = UserList([2, 3, 6])
alt1 = UserList([1, 1, 1])
print(aa < alt1)
print(aa > alt1)
aeq1 = UserList([3, 2, 6])
print(aeq1 == aa)
print(aeq1 != aa)
print(alt1 != aa)

