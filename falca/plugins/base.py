class BasePlugin:
    name: str = None

    def __init__(self, app) -> None:
        self.app = app
