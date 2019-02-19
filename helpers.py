#!/usr/bin/env python

from random import randint


class Powerhouse(object):
    def __init__(self, p_min, p_max, a, b, c, s):
        self.p_min = p_min
        self.p_max = p_max
        self.a = a
        self.b = b
        self.c = c
        self.s = s
        self.state = [
            randint(0, 1),
            randint(0, 1),
            randint(0, 1),
            randint(0, 1),
            randint(0, 1),
        ]

    @property
    def power(self):
        return self.calculate_power(self.level)

    @property
    def fuel_cost(self):
        return self.calculate_fuel_cost(self.power)

    @property
    def level(self):
        return self.calculate_level()

    def calculate_power(self, power_level):
        return self.p_min + (self.p_max - self.p_min) * power_level

    def calculate_fuel_cost(self, power):
        return self.a + self.b * power + self.c * pow(power, 2)

    def calculate_level(self):
        return self.calculate_integer_level() / 31

    def calculate_integer_level(self):
        return self.state[0] + 2 * self.state[1] + 4 * self.state[2] + 8 * self.state[3] + 16 * self.state[4]

    def level_increment(self):
        level = self.calculate_integer_level()
        if level >= 31:
            return False
        for index, value in enumerate(bin(level + 1)[2:]):
            self.state[-1 - index] = int(value)
        return True

    def level_decrement(self):
        level = self.calculate_integer_level()
        if level <= 0:
            return False
        for index, value in enumerate(bin(level - 1)[2:]):
            self.state[-1 - index] = int(value)
        return True


def get_state(candidate):
    return sum([powerhouse.state for powerhouse in candidate], [])


def apply_state(state, candidate):
    for powerhouse_index, start_index in enumerate(range(0, len(state), 5)):
        candidate[powerhouse_index].state = state[start_index:start_index + 5]


def apply_mutation(state):
    mutation_index = randint(0, len(state) - 1)
    state[mutation_index] = 0 if state[mutation_index] == 1 else 1


def one_point_crossing(input1, input2):
    crossing_point = randint(1, len(input1) - 1)
    result1 = input1[:crossing_point]
    result1.extend(input2[crossing_point:])
    result2 = input2[:crossing_point]
    result2.extend(input1[crossing_point:])

    return result1, result2


def calculate_epsilon(candidate, demand):
    power = 0
    power_lost = 0

    for powerhouse in candidate:
        power += powerhouse.power
        power_lost += powerhouse.s * pow(powerhouse.power, 2)

    return power - demand - power_lost


def network_cost(candidate):
    cost = 0
    for powerhouse in candidate:
        cost += powerhouse.fuel_cost
    return cost


def aim_function(candidate, demand, w):
    cost = network_cost(candidate)
    epsilon = calculate_epsilon(candidate, demand)
    # print(f'COST: {cost}, EPSILON: {epsilon}')
    return cost + w * abs(epsilon)

def fix_candidate(candidate, demand):
    epsilon = calculate_epsilon(candidate, demand)
    original_epsilon = epsilon
    # print(f'fixing candidate {epsilon}')
    if abs(epsilon) <= 100:
        return False
    if epsilon < 0:
        while epsilon < -100:
            # print('still in while increment?', epsilon)
            candidate_sorted = sorted(candidate, key=lambda x: x.level)
            if not any(powerhouse.level_increment() for powerhouse in candidate_sorted):
                return False
            epsilon = calculate_epsilon(candidate, demand)
            # print(f'Lowest powerhouse level incresed! Now epsilon: {epsilon}')
    else:
        while epsilon > 100:
            # print('still in while decrement?', epsilon)
            candidate_sorted = sorted(candidate, key=lambda x: x.level, reverse=True)
            if not any(powerhouse.level_decrement() for powerhouse in candidate_sorted):
                print('not called even once!')
                return False
            epsilon = calculate_epsilon(candidate, demand)
            # print(f'Biggest powerhouse level decreased! Now epsilon: {epsilon}')
    # print(f'Candidate fixed! Now epsilon {epsilon}, before {original_epsilon}')
