import inspect

from .base import BaseTest
from .comparators import compare_numbers
from .utils import HiddenPrints


class ClassTest(BaseTest):
    def __init__(
        self,
        namespace,
        class_name,
        reference_class=None,
        comparator=compare_numbers,
        r_tol=0,
        a_tol=0,
    ):
        super().__init__(namespace, r_tol, a_tol)
        self.class_name = class_name
        self.comparator = comparator
        self.reference_class = reference_class
        self.instance, self.target_instance = None, None

    def initialize_class(self, arg=None, args=None, kwargs=None):
        with HiddenPrints():
            klass = self.namespace[self.class_name]
            if arg is not None:
                self.instance = klass(arg)
                if self.reference_class is not None:
                    self.target_instance = self.reference_class(arg)
            elif args is not None:
                self.instance = klass(*args)
                if self.reference_class is not None:
                    self.target_instance = self.reference_class(*args)
            elif kwargs is not None:
                self.instance = klass(**kwargs)
                if self.reference_class is not None:
                    self.target_instance = self.reference_class(**kwargs)
            else:
                self.instance = klass()
                if self.reference_class is not None:
                    self.target_instance = self.reference_class()

    def is_instance(self, obj):
        return (
            not inspect.isroutine(obj)
            and not inspect.isclass(obj)
            and inspect.isclass(type(obj))
        )

    def is_class(self, obj):
        return inspect.isclass(obj)

    def has_method(self, method):
        return hasattr(self.namespace[self.class_name], method)

    def call_method(self, instance, test_case):
        method = getattr(instance, test_case["method"])
        if "arg" in test_case:
            return method(test_case["arg"])
        elif "args" in test_case:
            return method(*test_case["args"])
        elif "kwargs" in test_case:
            return method(**test_case["kwargs"])
        else:
            return method()

    def run_single_test_case(self, test_case):
        if "init" in test_case:
            if "arg" in test_case["init"]:
                self.initialize_class(arg=test_case["init"]["arg"])
            elif "args" in test_case["init"]:
                self.initialize_class(args=test_case["init"]["args"])
            elif "kwargs" in test_case["init"]:
                self.initialize_class(kwargs=test_case["init"]["kwargs"])
            else:
                self.initialize_class()
        if self.target_instance is None:
            target = test_case["target"]
        else:
            target = self.call_method(self.target_instance, test_case)
        if "comparator" in test_case:
            comparator = test_case["comparator"]
        else:
            comparator = self.comparator
        try:
            with HiddenPrints():
                result = self.call_method(self.instance, test_case)
                abs_error, rel_error = comparator(result, target)
                if abs_error <= self.a_tol or rel_error <= self.r_tol:
                    return True
            print(self.line)
            print(f"Test case {test_case} failed!")
            print(f"Expected:\n{target}\nGot:\n{result}")
            print(f"rel_error = {rel_error:.4e}, abs_error = {abs_error:.4e}\n")
        except Exception as e:
            print(self.line)
            print(f"Test with args {test_case} failed!\n{e}\n")
        return False

    def test(self, test_cases):
        n_passed = 0
        n_total = len(test_cases)
        print(self.double_line)
        print(f"Test for class {self.class_name}\n")
        if not self.is_defined(self.class_name):
            print(f"Class {self.class_name} is not defined!")
        elif not self.is_class(self.namespace[self.class_name]):
            print(f"{self.class_name} is not a class!")
        else:
            for test_case in test_cases:
                if self.run_single_test_case(test_case):
                    n_passed += 1

        print(self.double_line)
        print(f"{n_passed} / {n_total} tests passed!")
        print(self.double_line)
        return n_passed / n_total
