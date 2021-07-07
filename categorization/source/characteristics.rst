.. _characteristics:

Test Case Characteristics
=========================

By manually the accompanying
test case of each bug,
we identified what specific language features
are involved in each test case.
We group these language features into
eight general categories:

* *Standard Language Features*
* *Object-Oriented Programming (OOP) Features*
* *Functional Programming Features*
* *Parametric Polymorphism*
* *Type Inference Features*
* *Standard Library*
* *Other*

We discuss these categories and their
enclosing language features below.


Standard Language Features
--------------------------

This category includes features that can be found in every modern
programming language (e.g., method calls, arithmetic expressions, binary
operations, assignments, type casting, etc.).

Below you can find some standard features that
we encountered in the bug-revealing test cases.

Import
^^^^^^


The test case imports another source file.

Example:

.. code-block:: java
  :caption: mypackage/A.java

  class A {}

.. code-block:: java
  :caption: anotherpackage/B.java

  import myprocect.A;

  class B {}


Enums
^^^^^

The test case declares an enumeration.

Example:

.. code-block:: java

  enum Animal {
    DOG,
    CAT
  }


Arithmetic Expression
^^^^^^^^^^^^^^^^^^^^^

The test case involves arithmetic expressions.


Example:

.. code-block:: kotlin

  fun test(a: Int, b: Int) {
    val x = a + b 
  }


Augmented Assignment Operator
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The test case contains an augmented assignment operator (x += 1).


Example:

.. code-block:: kotlin

  fun test() {
    var x: Int = 1
    x += 1
  }

Variable Arguments
^^^^^^^^^^^^^^^^^^

The test cases declares a method with variable arguments.

Example:

.. code-block:: java

  class Test {
    void test(Integer x...) {}
  }


Cast
^^^^

The test case contains a cast expression.

Example:

.. code-block:: java

  class Test {
    void test() {
      Long x = (long) 1;
    }
  }


Array
^^^^^

The test case declares a variable, parameter or field whose
type is an array.

Example:

.. code-block:: java

  class Test {
    void test() {
      Integer[] x = new Integer[] {1};
    }
  }

Conditionals
^^^^^^^^^^^^

The test case involves conditionals (e.g., if, switch, ternary operator).

Example:

.. code-block:: kotlin

    open class A
    class B: A()
    fun test() =
      if (true) A() else B()

Loops
^^^^^

The test case contains loops (e.g., for, while).

Example:

.. code-block:: java

    class Test {
      void test(List<Integer> list) {
        for (Integer x: list) {}
      }
    }


Try / Catch
^^^^^^^^^^^

The test case contains try / catch statements or handles exceptions.

Example:

.. code-block:: java

  class Test {
    void test() {
      try {
        // something
      } catch (Exception e) {
        // something else
      }
    }
  }
