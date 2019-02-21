import unittest
from unittest import mock
from random import seed

from helpers import one_point_crossing, Powerhouse, calculate_epsilon, get_state, apply_state


class PowerhouseTestCase(unittest.TestCase):
    def setUp(self):
        seed(12341)
        self.powerhouse = Powerhouse(
            900,
            1200,
            1,
            pow(1, -3),
            pow(1, -6),
            pow(1, -8)
        )

    def test_general(self):
        powerhouse = Powerhouse(
            900,
            1200,
            1,
            2,
            3,
            1
        )
        powerhouse.state = [0, 0, 0, 0, 0]
        self.assertEqual(powerhouse.level, 0)
        self.assertEqual(powerhouse.power, 900)
        self.assertEqual(powerhouse.fuel_cost, 1 + 2 * 900 + 3 * 900 * 900)

    def test_level_increment(self):
        self.powerhouse.state = [0, 0, 0, 0, 0]
        self.assertEqual(self.powerhouse.calculate_integer_level(), 0)
        self.powerhouse.level_increment()
        self.assertEqual(self.powerhouse.calculate_integer_level(), 1)
        for i in range(35):
            self.powerhouse.level_increment()
        self.assertEqual(self.powerhouse.calculate_integer_level(), 31)

    def test_level_decrement(self):
        self.powerhouse.state = [1, 1, 1, 1, 1]
        self.assertEqual(self.powerhouse.calculate_integer_level(), 31)
        self.powerhouse.level_decrement()
        self.assertEqual(self.powerhouse.calculate_integer_level(), 30)
        for i in range(35):
            self.powerhouse.level_decrement()
        self.assertEqual(self.powerhouse.calculate_integer_level(), 0)


class OnePointCrossingTestCase(unittest.TestCase):
    @mock.patch('helpers.randint')
    def test_cross_tables(self, randint_mock):
        randint_mock.return_value = 3
        input1 = [1, 1, 1, 1, 1, 1]
        input2 = [0, 0, 0, 0, 0, 0]

        result1, result2 = one_point_crossing(input1, input2)

        self.assertListEqual(result1, [1, 1, 1, 0, 0, 0])
        self.assertListEqual(result2, [0, 0, 0, 1, 1, 1])


class CalculateEpsilonTestCase(unittest.TestCase):
    def setUp(self):
        self.powerhouse1 = Powerhouse(
            900,
            1200,
            1,
            2,
            3,
            1
        )
        self.powerhouse1.state = [0, 0, 0, 0, 0]

    def test_calculate_epsilon(self):
        demand = 950
        # at level 0 power is 900
        # s * power^2
        power_lost = 1 * 900 * 900
        # produced - demand - lost
        expected = 900 - demand - power_lost
        # 1 + 2 * 900 + 3 * 900 * 900
        result = calculate_epsilon([self.powerhouse1], demand)
        self.assertEqual(expected, result)

class HelpersTest(unittest.TestCase):
    def setUp(self):
        self.candidate = []
        seed(439230)
        self.powerhouse1 = Powerhouse(
            900,
            1200,
            1,
            pow(1, -3),
            pow(1, -6),
            pow(1, -8)
        )
        self.powerhouse2 = Powerhouse(
            950,
            1300,
            1,
            pow(1, -3),
            pow(1, -6),
            pow(1, -8)
        )
        self.candidate.append(self.powerhouse1)
        self.candidate.append(self.powerhouse2)

    def test_get_state(self):
        result = get_state(self.candidate)
        self.assertIsInstance(result, list)
        self.assertListEqual(result, self.powerhouse1.state + self.powerhouse2.state)

    def test_apply_state(self):
        test_state = [0, 1, 1, 0, 1, 0, 1, 0, 0, 1]
        apply_state(test_state, self.candidate)
        self.assertListEqual(self.powerhouse1.state, [0, 1, 1, 0, 1])
        self.assertListEqual(self.powerhouse2.state, [0, 1, 0, 0, 1])


if __name__ == '__main__':
    unittest.main()
