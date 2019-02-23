import matplotlib.pyplot as plt

from random import randint, sample, random
from helpers import generate_costs_matrix


def one_point_crossing(input1, input2):
    crossing_point = randint(1, len(input1) - 1)
    result1 = input1[:crossing_point]
    result1.extend(input2[crossing_point:])
    result2 = input2[:crossing_point]
    result2.extend(input1[crossing_point:])

    return result1, result2


CANDIDATES_COUNT = 100
MUTATION_FREQUENCY = 1 / 100

GENERATIONS_MAX_COUNT = 1000

NUMBER_OF_CITIES = 100

RANDOMNESS = 255

costs = generate_costs_matrix(NUMBER_OF_CITIES)

modified_mutation_frequency = MUTATION_FREQUENCY * 2


def generate_candidates(count):
    candidates = []
    for i in range(count):
        candidate = [randint(0, RANDOMNESS) for i in range(NUMBER_OF_CITIES)]
        candidates.append(candidate)
    return candidates


def get_traveling_order(candidate):
    data = [[] for i in range(RANDOMNESS + 1)]
    for index, number in enumerate(candidate):
        data[number].append(index)

    return sum(data, [])


def apply_mutation(candidate):
    mutation_index = randint(0, len(candidate) - 1)
    candidate[mutation_index] = randint(0, RANDOMNESS)


def get_cost(traveling_order, cost_matrix):
    cost = 0
    for i in range(len(traveling_order) - 2):
        cost += cost_matrix[traveling_order[i]][traveling_order[i + 1]]

    return cost

def do():
    generation_number = 0
    mutations_counter = 0

    population = generate_candidates(CANDIDATES_COUNT)

    results = []
    result_not_changed_counter = 0

    for i in range(GENERATIONS_MAX_COUNT):
        generation_number += 1
        print(f'Generation number: {generation_number}')

        population = sample(population, CANDIDATES_COUNT)
        for index in range(0, len(population), 2):
            candidate_1 = population[index]
            candidate_2 = population[index + 1]
            candidate_1, candidate_2 = one_point_crossing(candidate_1, candidate_2)

            if random() < modified_mutation_frequency:
                # print('INFO: Mutation applied!')
                mutations_counter += 1
                apply_mutation(candidate_1)

        population = sample(population, CANDIDATES_COUNT)

        new_population = []
        best_result = float('inf')

        for index in range(0, len(population), 2):
            candidate_1 = population[index]
            candidate_2 = population[index + 1]
            traveling_order_1 = get_traveling_order(candidate_1)
            traveling_order_2 = get_traveling_order(candidate_2)
            cost_1 = get_cost(traveling_order_1, costs)
            cost_2 = get_cost(traveling_order_2, costs)

            if cost_1 <= cost_2:
                new_population.append(candidate_1)
                if cost_1 < best_result:
                    best_result = cost_1
            else:
                new_population.append(candidate_2)
                if cost_2 < best_result:
                    best_result = cost_2

        print(f'The best result is: {best_result}')
        new_population.extend(generate_candidates(int(CANDIDATES_COUNT / 2)))

        population = new_population

        last_result = results[-1] if len(results) >= 1 else 0
        if abs(best_result - last_result) < 0.5:
            result_not_changed_counter += 1
        else:
            result_not_changed_counter = 0

        results.append(best_result)

        if result_not_changed_counter > 100:
            print(f'Not changed for a while! Break!')
            break

    print(f'Number of generations: {generation_number}')
    print(f'Number of applied mutations: {mutations_counter}')

    return results[-1]



results = []
SIMULATIONS_COUNT = 100

for i in range(SIMULATIONS_COUNT):
    results.append(do())


min_result = min(results)
max_result = max(results)

print(f'The best result is: {min_result}')

plt.plot([i + 1 for i in range(SIMULATIONS_COUNT)], results, 'ro')
plt.axis([0, SIMULATIONS_COUNT, min_result - min_result/10, max_result + max_result/10])
plt.xlabel('Simulation number')
plt.ylabel('Travel cost')
plt.show()
