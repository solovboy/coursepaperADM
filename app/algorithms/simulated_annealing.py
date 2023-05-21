import random
import math

from typing import List
from ..utils import AlgorithmState, calculate_distance


def simulated_annealing(
    graph: List[List[int]],
    initial_temperature: float = 100,
    alpha: float = 0.01,
    final_temperature: float = 0.1,
):
    current_path = [i for i in range(len(graph))]
    random.shuffle(current_path)

    current_distance = calculate_distance(graph, current_path)
    temperature = initial_temperature

    best_path = None
    best_distance = float("inf")

    while temperature >= final_temperature:
        new_path = current_path[:]
        a, b = random.randint(0, len(current_path) - 1), random.randint(
            0, len(current_path) - 1
        )
        new_path[a], new_path[b] = new_path[b], new_path[a]
        new_distance = calculate_distance(graph, new_path)
        cost_diff = new_distance - current_distance
        if random.uniform(0, 1) < math.exp(-1 * cost_diff / temperature):
            current_path = new_path
            current_distance = new_distance
        temperature -= alpha

        if new_distance < best_distance:
            best_path = new_path
            best_distance = new_distance

        yield AlgorithmState(
            solution=best_path,
            info=(
                f"Температура: {temperature:.2f}\n"
                f"Прогресс: {100 - int(100 * temperature / initial_temperature)}%"
            ),
        )
