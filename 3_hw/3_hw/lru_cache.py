import weakref


class LRUCache:
    class Element(object):
        """Класс хранимого элемента (это может быть все что душе угодно)"""
        __slots__ = ['prev', 'next', 'value', '__weakref__']  # для сокращения памяти использование слотов

        def __init__(self, value):
            """Так как Element является элементом двунаправленного списка, то содержит ссылки на предыдущий и следующий
            элементы, а также само значение"""
            self.prev, self.next, self.value = None, None, value

    class CacheStat:
        hit = 0
        miss = 0
        ratio = 0

        hit_set = 0
        miss_set = 0
        ratio_set = 0

        @classmethod
        def cache_info(cls):
            print(
                f'[ Hit: {cls.hit}. Miss: {cls.miss}. Efficiency: {round(cls.ratio, 3)} ] \
|| [ SET_hit: {cls.hit_set}. SET_miss: {cls.miss_set}. REFRESH_Efficiency: {round(cls.ratio_set, 3)} ]')

    def __init__(self, func=None, max_cache_size=2 ** 20):
        """Используется словарь со слабыми ссылками, чтобы объект действительно удалялся из памяти
        (кэш должен работать быстро и эффективно), иначе постепенно можно заполнить всю память"""
        self.dict = weakref.WeakValueDictionary()
        self.head = None
        self.tail = None
        self.count = 0
        self.maxCount = max_cache_size
        self.func = func  # объект-функция необходим при использовании класса как декоратора

    def _remove_element(self, element):
        """Удаление элемента из списка"""
        prev, next = element.prev, element.next
        if prev:  # если предыдущий элемент есть
            assert prev.next == element  # данную операцию можно вообще не делать
            # (проверяем, реально ли следующий элемент от предыдущего - наш элемент
            prev.next = next  # переставляем указатель на следующий элемент
        elif self.head == element:  # если предыдущего элемента нет, то проверяем, что элемент головной
            self.head = next  # переставляем начало списка на следующий за Element

        if next:  # если следующий элемент есть
            assert next.prev == element  # аналогичная проверка чисто для себя
            next.prev = prev  # переставляем указатель с предыдущего на элемент "через один" (аналогичное действие)
        elif self.tail == element:  # если это конец списка, то есть удаляем конечный элемент
            self.tail = prev  # то предыдущий элемент назначаем конечным
        element.prev, element.next = None, None  # зануляем все указатели у удаляемого элемента
        assert self.count >= 1  # проверяем, что кэш не был пуст
        self.count -= 1  # уменьшаем длину кэша после удаления элемента

    def _add_element(self, element):
        """Добавление элемента в список"""
        if element is None:  # с пустым элементом ничего не делаем
            return
        element.prev, element.next = self.tail, None  # добавляем в конец списка,
        # то есть предыдущим для нового элемента будет последний, а следующего пока нет
        if self.head is None:  # если вставляем в начало списка (кэш пуст)
            self.head = element  # то это головной элемент
        if self.tail is not None:  # если конец не пуст (то есть в кэше есть что-то)
            self.tail.next = element  # следующий за текущим конечным элементом является вставляемый
        self.tail = element  # назначение нового конца элемента
        self.count += 1  # увеличение длины кэша после вставки

    def get(self, key, *arg):
        """Аналог метода get для словаря (ведь кэш - ассоциативное запоминающее устройство,
         а значит, работает практически аналогично словарю"""
        element = self.dict.get(key, None)  # из словарика берем элемент по ключу
        if element:  # если элемент вообще есть
            self.hit_stat()
            self._remove_element(element)  # удаляем откуда-то мб из середины кэша
            self._add_element(element)  # и добавляем его в конец (делаем самым свежим)
            return element.value
        elif len(arg):  # если элемента не нашлось, то смотрим позиционные аргументы, если они есть
            self.miss_stat()
            return arg[0]  # то возвращаем первый аргумент в качестве значения по умолчанию
        else:
            self.miss_stat()
            raise KeyError("'%s' is not found in the dictionary", str(key))  # если и такого нет, то исключение

    def set(self, key, value):
        """Метод set для кэша"""
        self[key] = value

    def hit_stat(self):
        """Отмечаем, что произошло кэш-попадание"""
        self.CacheStat.hit += 1
        self.CacheStat.ratio = self.CacheStat.hit / (self.CacheStat.hit + self.CacheStat.miss)

    def miss_stat(self):
        """Отмечаем, что произошел кэш-промах"""
        self.CacheStat.miss += 1
        self.CacheStat.ratio = self.CacheStat.hit / (self.CacheStat.hit + self.CacheStat.miss)

    def hit_set_stat(self):
        """Отметка о кэш попадании при записи данных (то есть обновлении данных)"""
        self.CacheStat.hit_set += 1
        self.CacheStat.ratio_set = self.CacheStat.hit_set / (self.CacheStat.hit_set + self.CacheStat.miss_set)

    def miss_set_stat(self):
        """Отметка о кэш промахе при попытке записи данных"""
        self.CacheStat.miss_set += 1
        self.CacheStat.ratio_set = self.CacheStat.hit_set / (self.CacheStat.hit_set + self.CacheStat.miss_set)

    def __len__(self):
        return len(self.dict)

    def __getitem__(self, key):
        """Метод индексирования просто при получении"""
        element = self.dict[key]  # из словарика берется элемент по ключу
        self._remove_element(element)  # производится удаление элемента из кэша (мб где-то внутри)
        self._add_element(element)  # производится добавление как самого свежеиспользованного
        return element.value

    def __setitem__(self, key, value):
        """Метод индексирования с присваиванием"""
        try:
            element = self.dict[key]  # пытаемся вытащить элемент по ключу
            self.hit_set_stat()
            self._remove_element(element)  # и удалить его из кэша
        except KeyError:  # в случае, если такого ключа нет
            self.miss_set_stat()
            if self.count == self.maxCount:  # если достигнут лимит размера кэша
                self._remove_element(self.head)  # то удаляем самый старый элемент (сейчас он в голове списка)
        element = LRUCache.Element(value)  # теперь берется конструктор элемента по значению (это же новый элемент)
        self._add_element(element)  # элемент добавляется в кэш
        self.dict[key] = element  # и в сам словарик

    def __call__(self, *args, **kwargs):
        """Метод необходим для вызова класса как функции (в нашем случае чтобы использовать кэш как декоратор
        Хранение в словаре идет по типу
        key=(<функция>, (<позиционные аргументы>, замороженное множество пар <именованные аргументы>) )"""
        try:
            result = self.get((self.func, (args, frozenset(kwargs.items()))))  # ищем результат выполнения функции
            # по ней самой и по набору её параметров
        except KeyError:  # если не находим в кэше результатов, то
            result = self.func(*args, **kwargs)  # выполняем функцию с её аргументами
            self.set((self.func, (args, frozenset(kwargs.items()))), result)  # и заносим результат в кэш
            self.CacheStat.cache_info()
        return result

    def __del__(self):
        """Метод необходим, чтобы устранить утечку памяти, так как элементы находятся в списке,
         а значит, происходит ссылка элементо друг на друга и надо обнулять счетчики ссылок"""
        while self.head:
            self._remove_element(self.head)

    def __repr__(self):
        return f"{{{', '.join([' '.join([repr(key), repr(self.dict[key].value)]) for key in self.dict])}}}"

    def __str__(self):
        return f"{{{', '.join([': '.join([str(key), str(self.dict[key].value)]) for key in self.dict])}}}"


if __name__ == '__main__':
    a = LRUCache(max_cache_size=3)
    a[0] = 'szrfsrzf'
    a[1] = 'segdr'
    a[2] = [4, 5]
    a[3] = {3, 15}
    a['4'] = (88, 16, 32)
    a[(2, 3, 4)] = lambda x: x ** 2
    print(a)

    @LRUCache
    def fib(n):
        if n < 2:
            return n
        return fib(n - 1) + fib(n - 2)

    print([fib(n) for n in range(100)])

