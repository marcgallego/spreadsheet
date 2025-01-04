from .contents import Content


class Cell:
    def __init__(self) -> None:
        # TODO: decide if the identifier is needed
        self.content = None

    def set_value(self, content: Content) -> None:
        self.content = content

    def get_content(self) -> None | Content:
        return self.content

    def get_value(self) -> None | float:
        return self.content.get_value() if self.content else None
