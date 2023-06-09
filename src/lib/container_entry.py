class ContainerEntry:
    def __init__(self, cls, scope, instance=None):
        self.cls = cls
        self.scope = scope
        self.instance = instance
