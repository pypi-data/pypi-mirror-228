=====================
Experimental Features
=====================

Decorator for asserts
---------------------

Often you just want to write simple test cases using ``assert`` statements.
Asserts have the advantage that they are quick and easy to write. One disadvantage is that when one of many asserts fails, the other tests will not be executed.

For this we created a simple decorator. Here is an example:

.. code-block:: python
    :caption: A student answer

    # Student answer
    my_answer_a = 4
    my_answer_b = 18.3

And the test code

.. code-block:: python
    :caption: Testing using a decorator

    from e2xgradingtools.decorators import test_asserts

    @test_asserts(5) # The argument is the number of points this test is worth
    def my_test():
        assert my_answer_a == 5, "Wrong value for my_answer_a"
        assert my_answer_b == 18.3, "Wrong value for my_answer_b"
        
    my_test()

This will output:

::

    !--> AssertionError: Wrong value for my_answer_a
         Line 2: assert my_answer_a == 5, "Wrong value for my_answer_a"

    1 / 2 tests passed

    ### BEGIN GRADE
    2.5
    ### END GRADE

.. warning::
    When using the ``test_asserts`` decorator, it will count the number of asserts in the decorated function first.
    For this assert statements in loops are only counted once. Please only use this decorator if you are sure what you are doing.