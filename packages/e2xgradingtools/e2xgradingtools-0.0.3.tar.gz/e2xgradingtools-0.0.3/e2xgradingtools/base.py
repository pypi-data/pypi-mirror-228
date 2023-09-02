class BaseTest:
    def __init__(self, namespace, r_tol, a_tol):
        self.namespace = namespace
        self.r_tol = r_tol
        self.a_tol = a_tol
        self.line = "-" * 60
        self.double_line = "=" * 60

    def is_defined(self, name):
        return name in self.namespace

    def has_type(self, name, target_type):
        return isinstance(self.namespace[name], target_type)
