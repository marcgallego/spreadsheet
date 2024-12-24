from .contents import Content


class Cell:
    def __init__(self, id: str) -> None:
        self.id = id
        self.content = None

    def set_value(self, content) -> None:
        self.content = content

    def get_value(self) -> None | Content:
        return self.content
