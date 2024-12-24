from contents import Content


class Cell:
    def __init__(self, id: str):
        self.id = id
        self.content = None

    def set_content(self, content):
        self.content = content

    def get_content(self) -> None | Content:
        return self.content
