from .contents import Content
from .coordinates import Coordinates


class Cell:
    def __init__(self, coords: Coordinates) -> None:
        self.coordinates = coords
        self.content = None

    def set_value(self, content) -> None:
        self.content = content

    def get_value(self) -> None | Content:
        return self.content
