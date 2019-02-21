import matplotlib.pyplot as plt

from random import randint, sample, random
from helpers import generate_distances_matrix


def one_point_crossing(input1, input2):
    crossing_point = randint(1, len(input1) - 1)
    result1 = input1[:crossing_point]
    result1.extend(input2[crossing_point:])
    result2 = input2[:crossing_point]
    result2.extend(input1[crossing_point:])

    return result1, result2


CANDIDATES_COUNT = 100
MUTATION_FREQUENCY = 1 / 100

GENERATIONS_MAX_COUNT = 10000

NUMBER_OF_CITIES = 100

generation_number = 0
mutations_counter = 0

RANDOMNESS = 255

distances = generate_distances_matrix(NUMBER_OF_CITIES)

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


def get_distance(traveling_order, distance_matrix):
    distance = 0
    for i in range(len(traveling_order) - 2):
        distance += distance_matrix[traveling_order[i]][traveling_order[i + 1]]

    return distance


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
            print('INFO: Mutation applied!')
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
        distance_1 = get_distance(traveling_order_1, distances)
        distance_2 = get_distance(traveling_order_2, distances)

        if distance_1 <= distance_2:
            new_population.append(candidate_1)
            if distance_1 < best_result:
                best_result = distance_1
        else:
            new_population.append(candidate_2)
            if distance_2 < best_result:
                best_result = distance_2

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

plt.plot([i + 1 for i in range(generation_number)], results, 'ro')
plt.axis([0, generation_number, min(results) - 100, max(results) + 100])
plt.xlabel('Generations')
plt.ylabel('Travel cost')
plt.show()

