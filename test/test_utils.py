import unittest
import sys
import numpy as np

sys.path.append('../utils')

from utils import transform_list_into_categorical_vector_list as tlc, transform_categorical_vector_list_into_list as tcv, reshape_data_to_lstm


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

    def test_reshape_data_to_lstm(self):
        before_array = np.asarray([
            [0, 1],
            [0, 4],
            [0, 4],
            [0, 4],
            [0, 7],
            [0, 7],
            [0, 7],
            [0, 5],
            [0, 5],
            [2, 5],
            [2, 5],
            [2, 5],
            [2, 5],
            [2, 5],
            [3, 6],
            [3, 6],
            [3, 6],
            [3, 6],
            [3, 6],
            [3, 6],
        ])

        after_array = np.asarray([
            [
                [0, 1],
                [0, 1],
                [0, 1],
                [0, 1],
                [0, 1],
                [0, 1],
            ],
            [
                [0, 1],
                [0, 1],
                [0, 1],
                [0, 1],
                [0, 1],
                [0, 4],
            ],
            [
                [0, 1],
                [0, 1],
                [0, 1],
                [0, 1],
                [0, 4],
                [0, 4],
            ],
            [
                [0, 1],
                [0, 1],
                [0, 1],
                [0, 4],
                [0, 4],
                [0, 4],
            ],
            [
                [0, 1],
                [0, 1],
                [0, 4],
                [0, 4],
                [0, 4],
                [0, 7],
            ],
            [
                [0, 1],
                [0, 4],
                [0, 4],
                [0, 4],
                [0, 7],
                [0, 7],
            ],
            [
                [0, 4],
                [0, 4],
                [0, 4],
                [0, 7],
                [0, 7],
                [0, 7],
            ],
            [
                [0, 4],
                [0, 4],
                [0, 7],
                [0, 7],
                [0, 7],
                [0, 5],
            ],
            [
                [0, 4],
                [0, 7],
                [0, 7],
                [0, 7],
                [0, 5],
                [0, 5],
            ],
            [
                [0, 7],
                [0, 7],
                [0, 7],
                [0, 5],
                [0, 5],
                [2, 5],
            ],
            [
                [0, 7],
                [0, 7],
                [0, 5],
                [0, 5],
                [2, 5],
                [2, 5],
            ],
            [
                [0, 7],
                [0, 5],
                [0, 5],
                [2, 5],
                [2, 5],
                [2, 5],
            ],
            [
                [0, 5],
                [0, 5],
                [2, 5],
                [2, 5],
                [2, 5],
                [2, 5],
            ],
            [
                [0, 5],
                [2, 5],
                [2, 5],
                [2, 5],
                [2, 5],
                [2, 5],
            ],
            [
                [2, 5],
                [2, 5],
                [2, 5],
                [2, 5],
                [2, 5],
                [3, 6],
            ],
            [
                [2, 5],
                [2, 5],
                [2, 5],
                [2, 5],
                [3, 6],
                [3, 6],
            ],
            [
                [2, 5],
                [2, 5],
                [2, 5],
                [3, 6],
                [3, 6],
                [3, 6],
            ],
            [
                [2, 5],
                [2, 5],
                [3, 6],
                [3, 6],
                [3, 6],
                [3, 6],
            ],
            [
                [2, 5],
                [3, 6],
                [3, 6],
                [3, 6],
                [3, 6],
                [3, 6],
            ],
            [
                [3, 6],
                [3, 6],
                [3, 6],
                [3, 6],
                [3, 6],
                [3, 6],
            ],
        ])

        transformed_array = reshape_data_to_lstm(before_array, 6)
        self.assertListEqual(after_array.tolist(), transformed_array.tolist())

if __name__ == '__main__':
    unittest.main()
