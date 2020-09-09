import math
import unittest


class NdArray:

    def __init__(self, shape, data=list()):
        super().__init__()
        self.shape = shape
        self.data = data or [None for _ in range(math.prod(shape))]

    def __setitem__(self, coordinate, item):
        index = self.coordinate_to_index(coordinate=coordinate)
        self.data[index] = item

    def __getitem__(self, coordinate):
        index = self.coordinate_to_index(coordinate=coordinate)
        return self.data[index]

    def __str__(self):

        return "|".join([str(x) for x in self.data])

    def index_to_coordinate(self, index_list):

        answer_list = []

        for index in index_list:
            div = index

            coordinate = list()

            for dimension in self.shape:
                div, mod = divmod(div, dimension)
                coordinate.append(mod)

            answer_list.append(coordinate)

        return answer_list

    def coordinate_to_index(self, coordinate):
        summa = 0
        for k, n_k in enumerate(coordinate):
            N_l = math.prod(self.shape[:k])
            summa += N_l * n_k
        return summa


class TestNdArray(unittest.TestCase):

    def test_get(self):
        x = NdArray(shape=(2, 2), data=[0, 1, 2, 3])
        self.assertEqual([0, 2, 1, 3], [x[0, 0], x[0, 1], x[1, 0], x[1, 1]])

    def test_set(self):
        x = NdArray(shape=(3, 3, 3))
        x[1, 1, 1] = 5
        self.assertEqual(5, x[1, 1, 1])

    def testRecursiveList7(self):
        l = NdArray(shape=(10, 10))

        with self.subTest("zero"):
            self.assertEqual(0, l.coordinate_to_index([0, 0]))

        with self.subTest("one"):
            self.assertEqual(1, l.coordinate_to_index([1, 0]))

        with self.subTest("first axis rollover +1"):
            self.assertEqual(10, l.coordinate_to_index([0, 1]))

        with self.subTest("first axis rollover +2"):
            self.assertEqual(20, l.coordinate_to_index([0, 2]))

        with self.subTest("both rollover +1"):
            self.assertEqual(11, l.coordinate_to_index([1, 1]))

        with self.subTest("end of axis"):
            self.assertEqual(90, l.coordinate_to_index([0, 9]))

        with self.subTest("last spot"):
            self.assertEqual(99, l.coordinate_to_index([9, 9]))

    def testRecursiveList(self):
        l = NdArray(shape=[5])

        self.assertEqual([[1]], l.index_to_coordinate([1]), l)
        self.assertEqual([[0]], l.index_to_coordinate([5]), l)

    def testRecursiveList2(self):
        l = NdArray(shape=[1, 10])

        self.assertEqual([[0, 0]], l.index_to_coordinate([0]), l)
        self.assertEqual([[0, 1]], l.index_to_coordinate([1]), l)
        self.assertEqual([[0, 9]], l.index_to_coordinate([9]), l)
        self.assertEqual([[0, 0]], l.index_to_coordinate([10]), l)

    def testRecursiveList3(self):
        l = NdArray(shape=[10, 1])
        self.assertEqual([[0, 0]], l.index_to_coordinate([0]), l)
        self.assertEqual([[1, 0]], l.index_to_coordinate([1]), l)
        self.assertEqual([[9, 0]], l.index_to_coordinate([9]), l)
        self.assertEqual([[0, 0]], l.index_to_coordinate([10]), l)

    def testRecursiveList4(self):
        l = NdArray(shape=[10, 10])
        self.assertEqual([[0, 0]], l.index_to_coordinate([0]), l)
        self.assertEqual([[1, 0]], l.index_to_coordinate([1]), l)
        self.assertEqual([[2, 0]], l.index_to_coordinate([2]), l)
        self.assertEqual([[0, 1]], l.index_to_coordinate([10]), l)
        self.assertEqual([[1, 1]], l.index_to_coordinate([11]), l)
        self.assertEqual([[2, 1]], l.index_to_coordinate([12]), l)

        self.assertEqual([[8, 9]], l.index_to_coordinate([98]), l)
        self.assertEqual([[9, 9]], l.index_to_coordinate([99]), l)

    def testRecursiveList5(self):
        l = NdArray(shape=(7, 3, 11))
        self.assertEqual([[0, 0, 0]], l.index_to_coordinate([0]), l)
        self.assertEqual([[1, 0, 0]], l.index_to_coordinate([1]), l)

        self.assertEqual([[5, 1, 10]], l.index_to_coordinate([7 * 3 * 11 - 1 - 7 - 1]), l)
        self.assertEqual([[6, 1, 10]], l.index_to_coordinate([7 * 3 * 11 - 1 - 7]), l)

        self.assertEqual([[5, 2, 10]], l.index_to_coordinate([(7 * 3 * 11 - 1) - 1]), l)
        self.assertEqual([[6, 2, 10]], l.index_to_coordinate([7 * 3 * 11 - 1]), l)
