#!/usr/bin/env python
import matplotlib.pyplot as plt

from random import randint, uniform, random, sample

from helpers import Powerhouse, one_point_crossing, get_state, apply_mutation, apply_state, aim_function, fix_candidate

CANDIDATES_COUNT = 100
MUTATION_FREQUENCY = 1 / 1000

GENERATIONS_MAX_COUNT = 10000

POWERHOUSES_COUNT = 10
POWER_DEMAND = 10000

W_CONSTANT = 0.1

powerhouses_list = []

generation_number = 0
mutations_counter = 0


def generate_candidates(count):
    candidates = []
    for i in range(count):
        candidate = []
        for j in range(POWERHOUSES_COUNT):
            candidate.append(
                Powerhouse(
                    randint(500, 750),
                    randint(1000, 1250),
                    uniform(2.5, 7.5), # a
                    uniform(2.5, 7.5) * pow(10, -3), # b
                    uniform(2.5, 7.5) * pow(10, -6), # c
                    uniform(2.5, 7.5) * pow(10, -8) # s
                )
            )
        fix_candidate(candidate, POWER_DEMAND)
        candidates.append(candidate)
    return candidates


population = generate_candidates(CANDIDATES_COUNT)

# 1. crossing
# 2. mutation
# 3. selection
# 4. Check best result
# 5. generate new candidates

modified_mutation_frequency = MUTATION_FREQUENCY * 2


results = []
result_not_changed_counter = 0

# TODO: save data for 1st generation
for i in range(GENERATIONS_MAX_COUNT):
    # we are in the next generation - increase the generation counter
    generation_number += 1
    print(f'Generation number: {generation_number}')

    # 1. cross candidates
    # shuffle population to have random order
    population = sample(population, CANDIDATES_COUNT)

    # cross candidates and mutate
    for index in range(0, len(population), 2):
        candidate1 = population[index]
        candidate2 = population[index + 1]
        candidate1_state, candidate2_state = one_point_crossing(
            get_state(candidate1),
            get_state(candidate2)
        )
        # we have whole state here - lets try to apply mutation
        # Note: since we are iterating by 2 it means there is 2 time less
        # iterations through all candidates. That is why we are using modified_mutation_frequency
        # which has 2 times bigger probability
        if random() < modified_mutation_frequency:
            print('INFO: Mutation applied!')
            mutations_counter += 1
            apply_mutation(candidate1_state)

        # now write new state to candidates for further calculations
        apply_state(candidate1_state, candidate1)
        apply_state(candidate2_state, candidate2)

    # now we have to fix candidates with completely wrong setup
    for candidate in population:
        fix_candidate(candidate, POWER_DEMAND)

    # shuffle again
    population = sample(population, CANDIDATES_COUNT)
    # 3. selection
    # Not FIGHT!

    new_population = []
    best_result = float('inf')
    for index in range(0, len(population), 2):
        candidate1 = population[index]
        candidate2 = population[index + 1]
        result_1 = aim_function(candidate1, POWER_DEMAND, W_CONSTANT)
        result_2 = aim_function(candidate2, POWER_DEMAND, W_CONSTANT)

        if result_1 <= result_2:
            new_population.append(candidate1)
            if result_1 < best_result:
                best_result = result_1
        else:
            new_population.append(candidate2)
            if result_2 < best_result:
                best_result = result_1

    print(f'The best result is: {best_result}')
    new_population.extend(generate_candidates(int(CANDIDATES_COUNT / 2)))

    population = new_population

    last_result = results[-1] if len(results) >= 1 else 0
    if abs(best_result - last_result) < 0.5:
        result_not_changed_counter += 1
    else:
        result_not_changed_counter = 0

    results.append(best_result)

    if result_not_changed_counter > 50:
        print(f'Not changed for a while! Break!')
        break

print(f'Number of generations: {generation_number}')
print(f'Number of applied mutations: {mutations_counter}')

min_result = min(results)
max_result = max(results)
plt.plot([i + 1 for i in range(generation_number)], results, 'ro')
plt.axis([0, generation_number, min(results) - min(results) / 10, max(results) + max(results) / 10])
plt.xlabel('Generations')
plt.ylabel('Fuel cost')
plt.show()
