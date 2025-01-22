from .coordinates import Coordinates


class CircularDependencyException(Exception):
    def __init__(self) -> None:
        Exception.__init__(self)

    def __init__(self, msg) -> None:
        Exception.__init__(self, msg)


class DependencyManager:
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

    def _raise_circular_exception(self, cell: Coordinates) -> None:
        raise CircularDependencyException(
            f"Circular dependency detected when trying to set {cell}")

    def has_circular_dependency(self, start: Coordinates, depends_on: list[Coordinates]) -> None:
        if not depends_on:
            return

        temp_dependencies = self._dependencies.copy()

        for dependency in depends_on:
            if dependency not in temp_dependencies:
                temp_dependencies[dependency] = []
            temp_dependencies[dependency].append(start)

        visited = set()
        stack = set()

        def visit(cell) -> bool:
            if cell in stack:
                self._raise_circular_exception(start)
                return
            if cell in visited:
                return

            visited.add(cell)
            stack.add(cell)
            for neighbor in temp_dependencies.get(cell, []):
                if visit(neighbor):
                    return self._raise_circular_exception(start)
            stack.remove(cell)
            return

        return visit(start)
