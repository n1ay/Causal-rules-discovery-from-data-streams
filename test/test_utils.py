import unittest

from utils.utils import transfrom_list_into_categorical_vector_list as tlc, transfrom_categorical_vector_list_into_list as tcv


class UtilsTest(unittest.TestCase):
    def test_tlc(self):
        before_list = [0, 1, 2, 3, 4, 3, 2, 1, 0]
        after_list = [
            [1, 0, 0, 0, 0],
            [0, 1, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 1, 0],
            [0, 0, 0, 0, 1],
            [0, 0, 0, 1, 0],
            [0, 0, 1, 0, 0],
            [0, 1, 0, 0, 0],
            [1, 0, 0, 0, 0]
        ]

        transformed_list = tlc(before_list, max(before_list) + 1)

        self.assertListEqual(after_list, transformed_list)

    def test_tcv(self):
        before_list = [
            [1, 0, 0, 0, 0],
            [0, 1, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 1, 0],
            [0, 0, 0, 0, 1],
            [0, 0, 0, 1, 0],
            [0, 0, 1, 0, 0],
            [0, 1, 0, 0, 0],
            [1, 0, 0, 0, 0]
        ]
        after_list = [0, 1, 2, 3, 4, 3, 2, 1, 0]

        transformed_list = tcv(before_list)

        self.assertListEqual(after_list, transformed_list)