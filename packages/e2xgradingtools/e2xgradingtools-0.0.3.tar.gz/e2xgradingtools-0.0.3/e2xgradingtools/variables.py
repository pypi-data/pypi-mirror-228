from .base import BaseTest
from .comparators import compare_numbers


class VariableTest(BaseTest):
    def __init__(self, namespace, r_tol=0, a_tol=0):
        super().__init__(namespace, r_tol, a_tol)

    def test_variable(
        self, name, expected, expected_type=None, comparator=compare_numbers
    ):
        if not self.is_defined(name):
            return False, f"Variable {name} is not defined!"
        if expected_type is not None and not self.has_type(name, expected_type):
            return False, f"Variable {name} is not of type {expected_type}!"
        try:
            abs_error, rel_error = comparator(self.namespace[name], expected)
            if abs_error <= self.a_tol or rel_error <= self.r_tol:
                return True, ""
            error_msg = f"Expected {expected}\nGot {self.namespace[name]}\n"
            error_msg += f"rel_error = {rel_error:.4e}, abs_error = {abs_error:.4e}"
            return False, error_msg
        except Exception as e:
            return False, e

    def test(self, test_cases):
        n_passed = 0
        n_total = len(test_cases)

        print(self.double_line)
        print("Variable Test\n")
        for test_case in test_cases:
            status, msg = self.test_variable(**test_case)
            if status:
                n_passed += 1
            else:
                print(self.line)
                print("Test for variable {} failed\n{}".format(test_case["name"], msg))
                print(self.line)
                print()
        print(self.double_line)
        print(f"{n_passed} / {n_total} tests passed!")
        print(self.double_line)
        return n_passed / n_total
