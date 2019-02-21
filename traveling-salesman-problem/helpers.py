from random import randint


def generate_distances_matrix(count):
    matrix = [[0 for j in range(count)] for i in range(count)]

    for i in range(count):
        for j in range(i + 1, count):
            distance = randint(10, 100)
            matrix[i][j] = distance
            matrix[j][i] = distance
    return matrix
