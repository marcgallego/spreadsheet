from simple_spreadsheet.domain.coordinates import Coordinates


class UpdateManager:
    def __init__(self) -> None:
        self._dependencies = {}

    def _register_dependencies(self, cell: Coordinates, depends_on: list[Coordinates] | None) -> None:
        if depends_on is None:
            return
        for dependency in depends_on:
            if dependency not in self._dependencies:
                self._dependencies[dependency] = []
            self._dependencies[dependency].append(cell)

    def _remove_dependencies(self, cell) -> None:
        for dependency in self._dependencies:
            if cell in self._dependencies[dependency]:
                self._dependencies[dependency].remove(cell)

    def set_dependencies(self, cell, depends_on) -> None:
        self._remove_dependencies(cell)
        self._register_dependencies(cell, depends_on)

    def get_dependents(self, cell: Coordinates) -> list[Coordinates]:
        return self._dependencies.get(cell, [])
