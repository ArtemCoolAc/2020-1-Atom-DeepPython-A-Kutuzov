import unittest
from super_hash import SuperHash


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(SuperHash('sdzf*G*&Vdb87G^', " ", 3, 1).my_hash(),
                         SuperHash('sdzf*G*&Vdb87G^', " ", 3, 1).my_hash())
        self.assertEqual(SuperHash('dgzrsf').my_hash(), SuperHash('dgzrsf').my_hash())
        self.assertEqual(SuperHash("{3: 'abc', 5: 'ggg'})").my_hash(), SuperHash("{3: 'abc', 5: 'ggg'})").my_hash())
        self.assertEqual(SuperHash("[1,5,12,16,48]").my_hash(), SuperHash("[1,5,12,16,48]").my_hash())
        self.assertNotEqual(SuperHash("[1,2,3]").my_hash(), SuperHash("[3,2,1]").my_hash())
        self.assertNotEqual(SuperHash("123").my_hash(), SuperHash("(1,2,3)").my_hash())
        self.assertRaises(TypeError, SuperHash, ("drfse", 12))
        self.assertRaises(TypeError, SuperHash, ([2, 5, 1], ",", 5, 3))
        self.assertRaises(TypeError, SuperHash, ("drfse", "," "2", 4))
        self.assertRaises(TypeError, SuperHash, ("wew", ",", 2, "3"))
        # self.assertRaises(ValueError, SuperHash, ("qwe", "&", 11, 1))
        self.assertRaises(ValueError, lambda: SuperHash("qwe", "&", 11, 1))
        # self.assertRaises(TypeError, SuperHash.calculate_square("123", 1, 2, 3))
        self.assertRaises(TypeError, lambda: SuperHash.calculate_square("133", 1, 2, 3))
        self.assertRaises(TypeError, lambda: SuperHash.calculate_square(12344, "q", 2, 9))
        self.assertRaises(TypeError, lambda: SuperHash.calculate_square(12344, 4, "dg", 9))
        self.assertRaises(TypeError, lambda: SuperHash.calculate_square(12344, 12, 2, "awe"))


if __name__ == '__main__':
    unittest.main()
