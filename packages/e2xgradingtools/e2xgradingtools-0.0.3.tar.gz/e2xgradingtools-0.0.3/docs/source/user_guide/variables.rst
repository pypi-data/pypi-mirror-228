=================
Testing Variables
=================

The basic form of testing is the variable test, which is used to check if a student has correctly assigned values to one or more variables.

Setting up the test class
-------------------------

To set up the test class, we need to import the ``VariableTest`` and initialize it with the necessary parameters.

.. code-block:: python
    :caption: Initialize the test class

    from e2xgradingtools import VariableTest

    tester = VariableTest(
        namespace=globals(),
        r_tol=0.01, # The relative tolerance, defaults to 0
        a_tol=1     # The absolute tolerance, defaults to 0
    )

The ``VariableTest`` class requires the ``namespace`` parameter, which is set to ``globals()`` to indicate that the test should use the global namespace of the notebook. 
Additionally, we can set the relative and absolute tolerances for the test, which determine the acceptable margin of error for the expected values.

Anatomy of a test case
----------------------

Each test case is a Python dictionary. It has two required entries ``name`` and ``expected``, which specify the name of the variable that should be tested as a string and the expected value.

.. code-block:: python
    :caption: A single test case

    test_case = dict(
        name="my_variable",
        expected=5,
    )

Test cases can also include the type of the answer via the ``expected_type`` entry. 
Finally we can specify a ``comparator`` which is a function that compares the expected value to the actual value of the student. See the section about custom comparators for more information.

Examples of tests
-----------------

Consider a cell in which the student should give two answers ``my_answer_a`` and ``my_answer_b``:

.. code-block:: python
    :caption: A student answer

    # Student answer
    my_answer_a = 4
    my_answer_b = 18.3

A test would look like this:

.. code-block:: python
    :caption: A simple variable test

    from e2xgradingtools import VariableTest, grade_report

    tester = VariableTest(
        namespace=globals(),
        a_tol=0.2
    )

    test_cases = [
        dict(
            name="my_answer_a",
            expected=5
        ),
        dict(
            name="my_answer_b",
            expected=18.3,
        )
    ]

    percentage_passed = tester.test(test_cases)
    grade_report(percentage_passed, points=5) # Create a grade for this test, assuming the question is worth 5 points

The output of this test would then be:

::

    ============================================================
    Variable Test

    ------------------------------------------------------------
    Test for variable my_answer_a failed
    Expected 5
    Got 4
    rel_error = 2.0000e-01, abs_error = 1.0000e+00
    ------------------------------------------------------------

    ============================================================
    1 / 2 tests passed!
    ============================================================
    ### BEGIN GRADE
    2.5
    ### END GRADE




