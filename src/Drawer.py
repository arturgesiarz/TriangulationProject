"""
    Klasa sluzy wygodnemu wyswietlaniu naszych danych - beda tutaj dodawane metody
"""
from src.visualizer.main import Visualizer


class Drawer:
    def __init__(self):
        self.vis = Visualizer()

    def addVisRectanglePoints(self, vertexTab):
        self.vis.add_point(vertexTab, color="red")

    def addVisTrianglePoints(self, trianglePoints):
        self.vis.add_point(trianglePoints, color="pink")

    def show(self):
        self.vis.show()
