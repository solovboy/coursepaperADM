from typing import List

from .models import AlgorithmState


def calculate_distance(graph: List[List[int]], solution: List[int]):
    distance = 0
    for i in range(1, len(solution)):
        distance += graph[solution[i - 1]][solution[i]]
    return distance + graph[solution[-1]][solution[0]]
