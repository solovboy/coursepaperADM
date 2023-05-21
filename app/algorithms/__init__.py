from .simulated_annealing import simulated_annealing
from .ant_colony import ant_colony
from .tabu_search import tabu_search

ALGORITHMS = {
    "annealing": simulated_annealing,
    "ant_colony": ant_colony,
    "tabu_search": tabu_search,
}
