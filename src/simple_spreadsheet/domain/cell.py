from .contents import Content


class Cell:
    def __init__(self) -> None:
        self.content = None

    def set_content(self, content: Content) -> None:
        self.content = content

    def get_content(self) -> None | Content:
        return self.content

    def get_value_as_float(self) -> float:
        return self.content.get_value_as_float() if self.content else None

    def get_value_as_str(self) -> str:
        return self.content.get_value_as_str() if self.content else ''

    def get_value_to_dump(self) -> str:
        return self.content.get_value_to_dump() if self.content else ''
