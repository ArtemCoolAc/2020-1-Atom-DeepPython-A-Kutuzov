import weakref


class LRUCache:
    class Element(object):
        """Класс хранимого элемента (это может быть все что душе угодно"""
        __slots__ = ['prev', 'next', 'value', '__weakref__']  # для сокращения памяти использование слотов

        def __init__(self, value):
            """Так как Element является элементом двунаправленного списка, то содержит ссылки на предыдущий и следующий
            элементы, а также само значение"""
            self.prev, self.next, self.value = None, None, value

    def __init__(self, max_cache_size):
        """Используется словарь со слабыми ссылками, чтобы объект действительно удалялся из памяти
        (кэш должен работать быстро и эффективно), иначе постепенно можно заполнить всю память"""
        self.dict = weakref.WeakValueDictionary()
        self.head = None
        self.tail = None
        self.count = 0
        self.maxCount = max_cache_size

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
            self._remove_element(element)  # удаляем откуда-то мб из середины кэша
            self._add_element(element)  # и добавляем его в конец (делаем самым свежим)
            return element.value
        elif len(*arg):  # если элемента не нашлось, то смотрим позиционные аргументы, если они есть
            return arg[0]  # то возвращаем первый аргумент в качестве значения по умолчанию
        else:
            raise KeyError("'%s' is not found in the dictionary", str(key))  # если и такого нет, то исключение

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
            self._remove_element(element)  # и удалить его из кэша
        except KeyError:  # в случае, если такого ключа нет
            if self.count == self.maxCount:  # если достигнут лимит размера кэша
                self._remove_element(self.head)  # то удаляем самый старый элемент (сейчас он в голове списка)
        element = LRUCache.Element(value)  # теперь берется конструктор элемента по значению (это же новый элемент)
        self._add_element(element)  # элемент добавляется в кэш
        self.dict[key] = element  # и в сам словарик

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
    a = LRUCache(3)
    a[0] = 'szrfsrzf'
    a[1] = 'segdr'
    a[2] = [4, 5]
    a[3] = {3, 15}
    a['4'] = (88, 16, 32)
    print(a)
