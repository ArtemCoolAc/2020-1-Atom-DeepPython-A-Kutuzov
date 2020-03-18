class SuperHash:
    """Класс для вычисления интересного хэша"""
    error_message = ""

    def __init__(self, object_to_hash, separator='', words_in_hash_quantity=1, words_in_list_quantity=1):
        if type(object_to_hash) != str:
            raise TypeError("Object for hashing must be string")
        elif type(separator) != str:
            raise TypeError("Separator must be string even if it is a number")
        elif type(words_in_hash_quantity) != int:
            raise TypeError("Quantity of words inside the hash must be integer")
        elif type(words_in_list_quantity) != int:
            raise TypeError("Quantity of hashes must be integer")
        elif words_in_hash_quantity > 10 or words_in_hash_quantity < 1:
            raise ValueError("Quantity of words inside hash must be in range [1..10]")
        elif words_in_list_quantity > 10 or words_in_list_quantity < 1:
            raise ValueError("Quantity of hashes must be in range [1..10]")
        self.object = object_to_hash
        self.words_in_hash = words_in_hash_quantity  # inner
        self.words_in_list = words_in_list_quantity  # outer
        self.separator = separator
        self.object_to_hash = object_to_hash
        try:
            with open('words_alpha.txt') as word_file:
                self.valid_words = word_file.read().split()
                self.github_dict_length = len(self.valid_words)
        except EnvironmentError:
            self.error_message = "Something wrong with file"
            print(self.error_message)

    @staticmethod
    def calculate_square(my_hash, a=0, b=1, c=1):
        """Статический метод вычисления квадратного трехчлена от хэша с коэффициентами a,b,c"""
        if type(my_hash) != int or type(a) != int or type(b) != int or type(c) != int:
            raise TypeError("All numbers must be integer for calculating ax^2+bx+c")
        return a * my_hash ** 2 + b * my_hash + c

    def my_hash(self):
        """Логика вычисления хэша состоит в вычислении индексов с помощью смещений, вычисляемых при помощи
        квадратного трехчлена, затем производится индексирование по скинутому словарику слов, вычисленные индексы
        никогда не выйдут за пределы длины словарика, так как в конце берется остаток по модулю длины словаря"""
        if len(self.error_message) == 0:
            indices = list()
            start_hash = hash(self.object_to_hash)
            if type(start_hash) != int:
                raise TypeError("Something went wrong. Python Hash returned not int")
            for j in range(self.words_in_list):
                inner_indices = list()
                start_outer_hash = self.calculate_square(start_hash, 2, 3, 8) * (j + 1)
                for i in range(self.words_in_hash):
                    inner_indices.append(
                        self.calculate_square(start_outer_hash, 1, -5, 2) * (i + 1) % self.github_dict_length)
                indices.append(inner_indices)
            try:
                my_hash = [self.separator.join([self.valid_words[el].capitalize() for el in row]) for row in indices]
                return my_hash if self.words_in_list > 1 else my_hash[0]
            except Exception as e:
                print(e)
        else:
            print(f''' Method "{self.my_hash.__name__}" is already useless because "{self.error_message}"''')


if __name__ == '__main__':
    A = SuperHash('{23: "sdg", 46: "sdqqqq"}', " ", 10, 10)
    B = SuperHash('sdzf*G*&Vdb87G^', " ", 3, 1)
    C = SuperHash('sdzf*G*&Vdb87G^', " ", 3, 1)
    # A.my_hash()
    print(B.my_hash())
    print(C.my_hash() == B.my_hash())
