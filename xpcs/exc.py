class PacemakerError(Exception):
    pass


class NotFound(PacemakerError):
    pass


class NodeNotFound(NotFound):
    pass


class ResourceNotFound(NotFound):
    pass



