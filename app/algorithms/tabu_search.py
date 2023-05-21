import random

from typing import List
from ..utils import AlgorithmState, calculate_distance


def generate_neighborhood(solution: List[int]):
    neighborhood = []
    n_cities = len(solution)
    for i in range(1, n_cities - 1):
        for j in range(i + 1, n_cities):
            new_solution = solution.copy()
            new_solution[i], new_solution[j] = new_solution[j], new_solution[i]
            neighborhood.append(new_solution)
    return neighborhood


def tabu_search(
    graph: List[List[int]],
    n_iterations: int = 100,
    tabu_size: int = 20,
):
    n_cities = len(graph)
    current_solution = list(range(n_cities))
    random.shuffle(current_solution)

    best_solution = current_solution.copy()
    tabu_list = []

    for i in range(n_iterations):
        neighborhood = generate_neighborhood(current_solution)
        best_neighbor = None
        best_distance = float('inf')

        for neighbor in neighborhood:
            if neighbor not in tabu_list:
                distance = calculate_distance(graph, neighbor)
                if distance < best_distance:
                    best_neighbor = neighbor
                    best_distance = distance

        if best_neighbor is None:
            break

        current_solution = best_neighbor
        tabu_list.append(best_neighbor)
        if len(tabu_list) > tabu_size:
            tabu_list.pop(0)

        if calculate_distance(graph, best_neighbor) < calculate_distance(graph, best_solution):
            best_solution = best_neighbor

        yield AlgorithmState(
            info=f"Прогресс: {i + 1}/{n_iterations}",
            solution=best_solution,
        )
