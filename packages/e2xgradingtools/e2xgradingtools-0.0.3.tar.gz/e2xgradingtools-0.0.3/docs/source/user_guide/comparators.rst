==================
Custom Comparators
==================

By default all tests will assume that we want to test numbers. 
Often we might want to test more complex data types. For this you can define a custom comparator function.

Anatomy of a comparator
-----------------------

A comparator has two arguments, ``student_answer`` and ``expected_answer`` and returns a tuple of ``(absolute_error, relative_error)``.

Here is a custom comparator for testing sets:

.. code-block:: python

    def compare_sets(student_answer, expected_answer):
        common_elements = expected_answer.intersection(student_answer)
        
        rel_error = len(common_elements) / len(expected_answer)
        abs_error1 = abs(len(common_elements) - len(expected_answer))
        abs_error2 = abs(len(common_elements) - len(student_answer))


        return max(abs_error1, abs_error2), rel_error

Example 1 - Variable Test with custom comparator
------------------------------------------------

Here is an example of how we can use this comparator in a ``VariableTest``:

Student answer:

.. code-block:: python

    my_set = set([1, 2, 3, 4])

Test: 

.. code-block:: python

    from e2xgradingtools import VariableTest, grade_report

    tester = VariableTest(
        namespace=globals(),
        a_tol=0
    )

    percentage_passed = tester.test([
        dict(
            name="my_set",
            expected=set([1, 2, 3, 4, 5]),
            expected_type=set,
            comparator=compare_sets
        )
    ])

    grade_report(percentage_passed, points=10)

Output:

::

    ============================================================
    Variable Test

    ------------------------------------------------------------
    Test for variable my_set failed
    Expected {1, 2, 3, 4, 5}
    Got {1, 2, 3, 4}
    rel_error = 8.0000e-01, abs_error = 1.0000e+00
    ------------------------------------------------------------

    ============================================================
    0 / 1 tests passed!
    ============================================================
    ### BEGIN GRADE
    0.0
    ### END GRADE

Example 2 - Function Test with custom comparator
------------------------------------------------

Here is an example of how we can use this comparator in a ``FunctionTest``:

.. code-block:: python

    def create_even_set(my_list):
        return set(my_list)

.. code-block:: python

    from e2xgradingtools import FunctionTest, grade_report

    def create_even_set_ref(my_list):
        return set([elem for elem in my_list if elem % 2 == 0])

    tester = FunctionTest(
        namespace=globals(),
        function_name="create_even_set",
        reference_function=create_even_set_ref,
        comparator=compare_sets
    )

    percentage_passed = tester.test([
        dict(
            arg=[2, 4]
        ),
        dict(
            arg=[1, 2, 3, 4]
        )
    ])

    grade_report(percentage_passed, 10)

Output:

::

    ============================================================
    Test for function create_even_set

    ------------------------------------------------------------
    Test case {'arg': [1, 2, 3, 4]} failed!
    Expected:
    {2, 4}
    Got:
    {1, 2, 3, 4}
    rel_error = 1.0000e+00, abs_error = 2.0000e+00

    ============================================================
    1 / 2 tests passed!
    ============================================================
    ### BEGIN GRADE
    5.0
    ### END GRADE




