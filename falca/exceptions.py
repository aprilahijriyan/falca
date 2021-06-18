class FalcaError(Exception):
    pass


class PluginError(FalcaError):
    pass


class BadRouter(FalcaError):
    pass


class EndpointConflict(FalcaError):
    pass
