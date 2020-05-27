import unittest
from beautiful_multiply import calculate_mul
import random
from unittest.mock import Mock


class MyTestCase(unittest.TestCase):
    REPEATS_NUMBER = 100

    def test_constructor(self):
        self.assertRaises(TypeError, calculate_mul, ({2: 'srefse'}))
        self.assertRaises(ValueError, calculate_mul, ([3, 4, 15, 'sef', 3]))
        self.assertRaises(ArithmeticError, calculate_mul, ([]))

    def test_main_method(self):
        def generate_list():
            return [random.randint(1, 1000) for _ in range(random.randint(1, 1000))]

        mock = Mock(return_value=generate_list())

        for _ in range(self.REPEATS_NUMBER):
            # some_list = [random.randint(1,1000) for _ in range(random.randint(1,1000))]
            some_list = mock()
            A = calculate_mul(some_list)
            mul = 1
            for elem in some_list:
                mul *= elem
            B = [mul // elem for elem in some_list]
            self.assertEqual(A, B)

    def test_edge_cases(self):
        zero1 = [3, 5, 8, 0]
        res_zero1 = [0, 0, 0, 120]
        self.assertEqual(calculate_mul(zero1), res_zero1)
        zero2 = [0, 0, 0, 0, 0]
        res_zero2 = [0, 0, 0, 0, 0]
        self.assertEqual(calculate_mul(zero2), res_zero2)
        negative1 = [-1, 3, -2, 4]
        res_neg1 = [-24, 8, -12, 6]
        self.assertEqual(calculate_mul(negative1), res_neg1)


unittest.main()
