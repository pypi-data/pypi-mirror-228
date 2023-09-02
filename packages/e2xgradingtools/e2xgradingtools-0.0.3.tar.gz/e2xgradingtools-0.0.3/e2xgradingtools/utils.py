import sys


class HiddenPrints:
    def __enter__(self):
        self.original_stdout = sys.stdout
        sys.stdout = None

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout = self.original_stdout


def grade_report(coverage, points):
    print("### BEGIN GRADE")
    print(round(coverage * points, 1))
    print("### END GRADE")
