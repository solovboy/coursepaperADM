import random

from typing import List
from ..utils import AlgorithmState, calculate_distance


def ant_colony(
    graph: List[List[int]],
    n_iterations: int = 100,
    n_ants: int = 10,
    pheromone_weight: float = 1,
    distance_weight: float = 5,
    decay_rate: float = 0.95,
):
    n_cities = len(graph)
    pheromone = [
        [1 / (n_cities * n_cities) for _ in range(n_cities)] for _ in range(n_cities)
    ]

    shortest_path = None
    shortest_distance = float("inf")

    for i in range(n_iterations):
        paths = []
        distances = []

        for j in range(n_ants):
            path = []
            unvisited_cities = list(range(n_cities))
            current_city = random.choice(unvisited_cities)
            unvisited_cities.remove(current_city)
            path.append(current_city)

            while unvisited_cities:
                probabilities = []
                total_prob = 0

                for city in unvisited_cities:
                    numerator = pheromone[current_city][city] ** pheromone_weight
                    denominator = graph[current_city][city] ** distance_weight
                    probabilities.append(numerator / denominator)
                    total_prob += numerator / denominator

                probabilities = [prob / total_prob for prob in probabilities]
                next_city = random.choices(unvisited_cities, probabilities)[0]

                path.append(next_city)
                unvisited_cities.remove(next_city)
                current_city = next_city

            paths.append(path)
            distances.append(calculate_distance(graph, path))

        min_distance = min(distances)
        if min_distance < shortest_distance:
            shortest_distance = min_distance
            shortest_path = paths[distances.index(min_distance)]

        delta_pheromone = [[0 for _ in range(n_cities)] for _ in range(n_cities)]
        for path, distance in zip(paths, distances):
            for j in range(n_cities - 1):
                delta_pheromone[path[j]][path[j + 1]] += 1 / distance
            delta_pheromone[path[-1]][path[0]] += 1 / distance

        for j in range(n_cities):
            for k in range(n_cities):
                pheromone[j][k] = pheromone[j][k] * decay_rate + delta_pheromone[j][k]

        yield AlgorithmState(
            info=f"Поколение {i + 1}/{n_iterations}", solution=shortest_path
        )
