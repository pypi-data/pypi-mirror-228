=================
Testing Functions
=================

Often we want a student to provide an answer in the form of a function. For this we can use the ``FunctionTest`` class.

Setting up the test class
-------------------------

First we need to set up our test class

.. code-block:: python
    :caption: Initialize the test class

    from e2xgradingtools import FunctionTest

    def my_square(x):
        return x*x

    tester = FunctionTest(
        namespace=globals(),
        function_name="square",       # The name of the student function
        reference_function=my_square, # An optional reference implementation to test against
        r_tol=0.01,                   # The relative tolerance, defaults to 0
        a_tol=1                       # The absolute tolerance, defaults to 0
    )

Similar to a ``VariableTest``, a ``FunctionTest`` has a namespace and absolute and relative tolerances. 
It also receives the ``function_name`` of the student function to test as a string.

Additionally it can be supplied with a custom ``comparator`` function, that takes the student answer and expected answer and returns an absolute and relative error.
More about comparators can be found in the comparator section of the docs.

Anatomy of a test case
----------------------

Each test case is a Python dictionary. It receives the argument of the student function in one of three ways.
This can be a single argument to the function specified with ``arg``, a list of arguments specified with ``args`` or a dictionary of named arguments specified with ``kwargs``.


.. code-block:: python
    :caption: A single test case

    test_case = dict(
        arg=5
    )

If a ``reference_function`` was provided, the tester will take the return value of the reference_function as the expected value.
If no ``reference_function`` is provided, or you want to test against a specific output without calling the ``reference_function``, this can be specified with the ``target`` argument:

.. code-block:: python
    :caption: A single test case with expected value

    test_case = dict(
        arg=5,
        target=25
    )

Sometimes we want to perform probabilistic tests that might not always pass. For this we can pass the parameter ``max_reruns``, that specifies how often the test is repeated until it is marked as failed.

Example 1 - Function fails with some arguments
----------------------------------------------

The student answer:

.. code-block:: python
    :caption: A simple student answer

    def square(x):
        if x < 7:
            return x*x
        return 70

The test:

.. code-block:: python
    :caption: Test for student answer

    from e2xgradingtools import FunctionTest, grade_report

    def square_ref(x):
        return x**2

    tester = FunctionTest(
        namespace=globals(),
        function_name="square",
        reference_function=square_ref
    )

    test_cases = [
        dict(
            arg=5
        ),
        dict(
            arg=-3,
            target=9
        ),
        dict(
            args=[8]
        )
    ]

    percentage_passed = tester.test(test_cases)
    grade_report(percentage_passed, points=10)

Output:

::

    ============================================================
    Test for function square

    ------------------------------------------------------------
    Test case {'args': [8]} failed!
    Expected:
    64
    Got:
    70
    rel_error = 9.3750e-02, abs_error = 6.0000e+00

    ============================================================
    2 / 3 tests passed!
    ============================================================
    ### BEGIN GRADE
    6.7
    ### END GRADE


Example 2 - Function has no return statement
--------------------------------------------

The student answer:

.. code-block:: python
    :caption: A student answer without a return statement

    def square(x):
        print(x*x)

The test:

.. code-block:: python
    :caption: Test for student answer

    from e2xgradingtools import FunctionTest, grade_report

    def square_ref(x):
        return x**2

    tester = FunctionTest(
        namespace=globals(),
        function_name="square",
        reference_function=square_ref
    )

    test_cases = [
        dict(
            arg=5
        ),
        dict(
            arg=-3,
            target=9
        ),
        dict(
            args=[8]
        )
    ]

    percentage_passed = tester.test(test_cases)
    grade_report(percentage_passed, points=10)

Output:

::

    ============================================================
    Test for function square

    square does not have a return statement!
    ============================================================
    0 / 3 tests passed!
    ============================================================
    ### BEGIN GRADE
    0.0
    ### END GRADE


Example 3 - Function is not defined
-----------------------------------

The student answer:

.. code-block:: python
    :caption: A student answer with a misspelled function

    def square1(x):
        return x*x

The test:

.. code-block:: python
    :caption: Test for student answer

    from e2xgradingtools import FunctionTest, grade_report

    def square_ref(x):
        return x**2

    tester = FunctionTest(
        namespace=globals(),
        function_name="square",
        reference_function=square_ref
    )

    test_cases = [
        dict(
            arg=5
        ),
        dict(
            arg=-3,
            target=9
        ),
        dict(
            args=[8]
        )
    ]

    percentage_passed = tester.test(test_cases)
    grade_report(percentage_passed, points=10)

Output:

::

    ============================================================
    Test for function square

    Function square is not defined!
    ============================================================
    0 / 3 tests passed!
    ============================================================
    ### BEGIN GRADE
    0.0
    ### END GRADE


Example 4 - Student function has a lot of print statements
----------------------------------------------------------

Often students have some debug print statements in their code that clutters our tests.
By default all print statements in student functions are ignored during testing:

The student answer:

.. code-block:: python
    :caption: A student answer with print statements

    def square(x):
        print("="*20)
        print("DEBUG")
        return x*x

The test:

.. code-block:: python
    :caption: Test for student answer

    from e2xgradingtools import FunctionTest, grade_report

    def square_ref(x):
        return x**2

    tester = FunctionTest(
        namespace=globals(),
        function_name="square",
        reference_function=square_ref
    )

    test_cases = [
        dict(
            arg=5
        ),
        dict(
            arg=-3,
            target=9
        ),
        dict(
            args=[8]
        )
    ]

    percentage_passed = tester.test(test_cases)
    grade_report(percentage_passed, points=10)

Output:

::

    ============================================================
    Test for function square

    ============================================================
    3 / 3 tests passed!
    ============================================================
    ### BEGIN GRADE
    10.0
    ### END GRADE
