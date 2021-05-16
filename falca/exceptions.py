class FalcaError(Exception):
    pass


class PluginNotFound(FalcaError):
    pass


class BadRouter(FalcaError):
    pass


class EndpointConflict(FalcaError):
    pass
