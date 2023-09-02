import ast
import inspect

from .base import BaseTest
from .comparators import compare_numbers
from .utils import HiddenPrints


class FunctionTest(BaseTest):
    def __init__(
        self,
        namespace,
        function_name,
        reference_function=None,
        comparator=compare_numbers,
        r_tol=0,
        a_tol=0,
    ):
        super().__init__(namespace, r_tol, a_tol)
        self.fun_name = function_name
        self.comparator = comparator
        self.reference_function = reference_function

    def is_callable(self):
        return callable(self.namespace[self.fun_name])

    def has_return_statement(self):
        return any(
            isinstance(node, ast.Return)
            for node in ast.walk(
                ast.parse(inspect.getsource(self.namespace[self.fun_name]))
            )
        )

    def call_function(self, function, test_case):
        if "arg" in test_case:
            return function(test_case["arg"])
        elif "args" in test_case:
            return function(*test_case["args"])
        elif "kwargs" in test_case:
            return function(**test_case["kwargs"])

    def run_single_test_case(self, test_case):
        if "target" in test_case:
            target = test_case["target"]
        else:
            target = self.call_function(self.reference_function, test_case)

        max_reruns = 1
        if "max_reruns" in test_case:
            max_reruns = test_case["max_reruns"]
        try:
            with HiddenPrints():
                for _ in range(max_reruns):
                    result = self.call_function(
                        self.namespace[self.fun_name], test_case
                    )
                    abs_error, rel_error = self.comparator(result, target)
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
        print(f"Test for function {self.fun_name}\n")
        if not self.is_defined(self.fun_name):
            print(f"Function {self.fun_name} is not defined!")
        elif not self.is_callable():
            print(f"{self.fun_name} is not callable!")
        elif not self.has_return_statement():
            print(f"{self.fun_name} does not have a return statement!")
        else:
            for test_case in test_cases:
                if self.run_single_test_case(test_case):
                    n_passed += 1

        print(self.double_line)
        print(f"{n_passed} / {n_total} tests passed!")
        print(self.double_line)
        return n_passed / n_total
