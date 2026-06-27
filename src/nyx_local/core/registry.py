class Registry:
    """Simple component registry for application bootstrap wiring."""

    def __init__(self) -> None:
        self._components: dict[str, object] = {}

    def register(self, name: str, component: object) -> None:
        self._components[name] = component

    def get(self, name: str) -> object:
        return self._components[name]

    def clear(self) -> None:
        self._components.clear()
