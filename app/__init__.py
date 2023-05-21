import math

from .ui import Ui_MainWindow
from PIL import Image, ImageDraw
from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.QtGui import QPixmap
from io import BytesIO
from typing import List, Optional

from .utils import calculate_distance
from .utils.defaults import DEFAULT_GRAPH, BEST_DISTANCE
from .algorithms import ALGORITHMS
from .utils.models import AlgorithmState

ALGORITHM_INDEXES = ["annealing", "ant_colony", "tabu_search"]


class MainWindow(QMainWindow):
    city_count: int
    graph: List[List[int]]
    running: bool = False

    options: dict
    current_path: Optional[List[int]]

    def __init__(self):
        super().__init__()

        self.canvas = Image.new("RGB", size=(512, 512), color=(255, 255, 255))
        self.draw = ImageDraw.Draw(self.canvas, mode="RGBA")

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.city_count = 25
        self.graph = DEFAULT_GRAPH
        self.options = {}
        self.current_path = None

        self.ui.initialTemperature.valueChanged.connect(
            self.set_option("annealing", "initial_temperature")
        )
        self.ui.stepTemperature.valueChanged.connect(
            self.set_option("annealing", "alpha")
        )
        self.ui.finalTemperature.valueChanged.connect(
            self.set_option("annealing", "final_temperature")
        )

        self.ui.antIterationCount.valueChanged.connect(
            self.set_option("ant_colony", "n_iterations")
        )
        self.ui.antCount.valueChanged.connect(self.set_option("ant_colony", "n_ants"))

        self.ui.tabuIterationCount.valueChanged.connect(self.set_option("tabu_search", "n_iterations"))
        self.ui.tabuSize.valueChanged.connect(self.set_option("tabu_search", "tabu_size"))

        self.ui.stopButton.setEnabled(False)

        self.ui.stopButton.clicked.connect(self.stop_algorithm)
        self.ui.startButton.clicked.connect(self.start_algorithm)

        self.draw_graph()
        self.show()

    def stop_algorithm(self):
        self.running = False
        self.ui.stopButton.setEnabled(False)
        self.ui.startButton.setEnabled(True)

    def start_algorithm(self):
        self.ui.stopButton.setEnabled(True)
        self.ui.startButton.setEnabled(False)

        self.running = True
        algorithm = ALGORITHM_INDEXES[self.ui.tabs.currentIndex()]
        for state in ALGORITHMS[algorithm](
            self.graph, **self.options.get(algorithm, {})
        ):
            state: AlgorithmState
            if not self.running:
                break
            self.current_path = state.solution
            distance = calculate_distance(self.graph, self.current_path)

            self.draw_graph()
            self.ui.info.setPlainText(
                f"{state.info}\n\n"
                f"Текущее расстояние: {distance}\n"
                f"Отклонение от оптимального: +{100 * distance / BEST_DISTANCE - 100:.2f}%\n\n"
                f"Текущий путь:\n{' - '.join(str(i + 1) for i in self.current_path)}"
            )
            QApplication.processEvents()

        self.running = False
        self.ui.stopButton.setEnabled(False)
        self.ui.startButton.setEnabled(True)

    def set_option(self, algorithm: str, option: str):
        if algorithm not in self.options:
            self.options[algorithm] = {}

        def callback(value):
            self.options[algorithm][option] = value

        return callback

    def update_city_count(self, update: int):
        self.city_count = update

    def draw_graph(self):
        self.canvas.paste((255, 255, 255), (0, 0, 512, 512))  # type: ignore

        city_coords = []

        for i in range(self.city_count):
            phi = 2 * math.pi * i / self.city_count
            city_coords.append(
                (256 + int(math.cos(phi) * 448 / 2), 256 + int(math.sin(phi) * 448 / 2))
            )

        if self.current_path is not None:
            for i in range(1, len(self.current_path)):
                x1, y1 = city_coords[self.current_path[i - 1]]
                x2, y2 = city_coords[self.current_path[i]]

                self.draw.line((x1, y1, x2, y2), width=3, fill=(255, 0, 196, 255))

            x1, y1 = city_coords[self.current_path[-1]]
            x2, y2 = city_coords[self.current_path[0]]
            self.draw.line((x1, y1, x2, y2), width=3, fill=(255, 0, 196, 255))

        for i, (x, y) in enumerate(city_coords):
            self.draw.ellipse((x - 9, y - 9, x + 9, y + 9), fill=(0, 0, 0, 255))

            w, h = self.draw.textsize(f"{i + 1}")
            self.draw.text(
                (x - 8 + (19 - w) / 2, y - 9 + (19 - h) / 2),
                text=f"{i + 1}",
                fill="white",
            )

        io = BytesIO()
        self.canvas.save(io, format="PNG")
        pixmap = QPixmap()
        pixmap.loadFromData(io.getvalue(), "PNG")
        self.ui.canvas.setPixmap(pixmap)
