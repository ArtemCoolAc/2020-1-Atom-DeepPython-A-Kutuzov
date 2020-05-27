import random
import heapq


class Median:
    def __init__(self, data):
        self.data = data
        self.min_heap = []
        self.max_heap = []
        self.medians = []

    def simplest_way(self):
        analyzed_now_list = list()
        medians = list()
        for elem in self.data:
            analyzed_now_list.append(elem)
            sorted_data = list(sorted(analyzed_now_list))
            length = len(sorted_data)
            if length % 2 != 0:
                medians.append(sorted_data[length // 2])
            else:
                medians.append((sorted_data[length // 2] + sorted_data[length // 2 - 1]) / 2)
        return medians

    def _add_numbers(self, elem):
        """В MAX_heap хранятся МИНИМАЛЬНЫЕ элементы и самый большой из них - корень
        В MIN_heap хранятся МАКСИМАЛЬНЫЕ элементы и самый маленький из них - корень"""
        if len(self.max_heap) == 0 or elem < self.max_heap[0]:  # если элемент меньше минимального из максимальных
            heapq.heappush(self.max_heap, elem)  # вставляем его в кучу к минимальным
            heapq._heapify_max(self.max_heap)  # heappush работает для heapmin, надо отдельно восстановить свойства
        else:  # иначе вставляем к большим элементам
            heapq.heappush(self.min_heap, elem)
            heapq.heapify(self.min_heap)

    def _rebalance(self):
        """Суть метода ребаланса: определить большую и меньшую кучи, если разница в их размере больше 1, то делаем
        перекидывание вершины кучи из большей в меньшую, то есть если большая - с меньшими элементами, то к меньшей
        с большими элементами уйдет максимальный из меньших элементов, соответственно, если большая куча
        с большими элементами, то в меньшую кучу с меньшими элементами уйдет минимальный из больших,
        таким образом на пиках куч всегда содержатся срединные элементы некоторого потока, и в случае если длины
        не равны, то медианой будет вершины большей по размеру кучи, иначе среднее арифметическое пиков двух куч"""
        flag_max = True
        max_heap_length = len(self.max_heap)
        min_heap_length = len(self.min_heap)
        bigger_heap = self.max_heap if max_heap_length > min_heap_length else self.min_heap
        flag_max = True if max_heap_length > min_heap_length else False
        smaller_heap = self.min_heap if max_heap_length > min_heap_length else self.max_heap
        if len(bigger_heap) - len(smaller_heap) >= 2:
            if flag_max:  # то есть большая куча является max_heap (protected), меньшая min_heap (default)
                heapq.heappush(smaller_heap, heapq._heappop_max(bigger_heap))
            else:
                heapq.heappush(smaller_heap, heapq.heappop(bigger_heap))
                heapq._heapify_max(smaller_heap)  # heappush не работает нормально с heap_max, восстанавливаем кучу

    def _get_median(self):
        """В случае если длины куч не равны, то медианой будет вершина большей по размеру кучи,
        иначе среднее арифметическое вершин двух куч,
        то есть максимального из меньших элементов и минимального из больших"""
        max_heap_length = len(self.max_heap)
        min_heap_length = len(self.min_heap)
        bigger_heap = self.max_heap if max_heap_length > min_heap_length else self.min_heap
        smaller_heap = self.min_heap if max_heap_length > min_heap_length else self.max_heap
        if len(bigger_heap) == len(smaller_heap):
            return (bigger_heap[0] + smaller_heap[0]) / 2
        else:
            return bigger_heap[0]

    def using_heaps_now(self):
        """Строятся две кучи: MAX_heap и MIN_heap. В MAX_heap заносятся меньшие элементы, в MIN_heap - большие.
        При этом если у одной кучи будет перекос по длине, будет произведен сдвиг с одной кучи до другой"""
        for elem in self.data:
            self._add_numbers(elem)
            self._rebalance()
            self.medians.append(self._get_median())
        return self.medians

    def add_number(self, elem: int):
        self._add_numbers(elem)
        self._rebalance()
        self.medians.append(self._get_median())
        return self.medians


if __name__ == '__main__':
    answers = list()
    for _ in range(50):
        A = Median([random.randint(0, 1000) for _ in range(random.randint(1000, 2000))])
        medians = A.simplest_way()
        medians_advanced = A.using_heaps_now()
        answers.append(medians == medians_advanced)
    print(all(answers))

