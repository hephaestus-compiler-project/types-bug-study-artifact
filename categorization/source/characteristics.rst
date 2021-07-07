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

Object-Oriented Programming (OOP) Features
------------------------------------------

This category includes features that are related to object-oriented
programming, e.g., classes, fields, methods, inheritance, object
initialization, overriding, etc.

Below you can find some OOP features that
we encountered in the bug-revealing test cases.

Inheritance
^^^^^^^^^^^

The test case declares a class that inherits from another.

Example:

.. code-block:: kotlin

    open class A
    class B: A()

Multiple Implements
^^^^^^^^^^^^^^^^^^^

The test case declares a class that implements more than one
interfaces.

Example:

.. code-block:: kotlin

	interface A
	interface B
	class B: A, B


Access Modifier
^^^^^^^^^^^^^^^

The test case uses access modifiers keywords (e.g., private)

.. code-block:: java

    class Test {
      private Test() {}
    }


Nested Class
^^^^^^^^^^^^

The test case contains a class which is declared inside the body
of another class.

.. code-block:: java

    class A {
     class B {}
    }

Anonymous Class
^^^^^^^^^^^^^^^

The test case declares an anonymous class.

.. code-block:: java

  interface Foo {
    String foo();
  }
  class Test {
    void test() {
      Foo x = new Foo() {
        public String foo() { return "v"; }
      };
    }
  }


Overriding
^^^^^^^^^^

The test case contains a class that overrides a specific method or field.

Example:

.. code-block:: kotlin

    open class A {
      open fun foo() = "A"
    }
    class B: A() {
      override fun foo() = "B"
    }


Overloading
^^^^^^^^^^^

The test case contains overloaded methods.

Example:

.. code-block:: kotlin

    class A {
      fun test(): String = "test A"
      fun test(x: String) = x
    }

Singleton Object
^^^^^^^^^^^^^^^^

The test case declares a singleton object (Scala and Kotlin only).

Example:

.. code-block:: scala

  object A {}


Static Method
^^^^^^^^^^^^^

The test case declares a static method (Groovy and Java only).

Example:

.. code-block:: java

    class Test {
      public static void test() {}
    }


Secondary Constructor
^^^^^^^^^^^^^^^^^^^^^

The test case declares a secondary constructor (Kotlin only).

Example:

.. code-block:: kotlin

    class A {
      constructor(x: Int) {}
    }


Sealed Class
^^^^^^^^^^^^

The test case declares a sealed class.

Example:

.. code-block:: kotlin

  sealed class A {}


Data Class
^^^^^^^^^^

The test case declares a data class (Kotlin only).

Example:

.. code-block:: kotlin

    data class A(val x: Int)

Case Class
^^^^^^^^^^

The test case declares a case class (Scala only).

Example:

.. code-block:: scala

  case class A(x: String)


Value Class
^^^^^^^^^^^

The test case declares a value class (Scala only).

Example:

.. code-block:: scala

  class A(val x: String) extends AnyVal



This
^^^^

The test case uses the `this` expression.

Example:

.. code-block:: kotlin

  class A {
    constructor(x: Int): this() {}
  }



Self types
^^^^^^^^^^

The test case uses self types (Scala only).

Example:

.. code-block:: scala

	trait A {
	  def x: String
	}

	trait B {
	  this: A =>  // reassign this
	  def foo() = ???
	}

Property Reference
^^^^^^^^^^^^^^^^^^

The test case contains a reference to a property of class.

Example:

.. code-block:: kotlin

    class A(val x: Int)
    fun test() {
      val x = A()
      x::x
    }


Delegation
^^^^^^^^^^

The test case uses the delegation functionality (Kotlin only).

Example:

.. code-block:: kotlin

  interface Base {
    fun print()
  }

  class BaseImpl(val x: Int) : Base {
    override fun print() { print(x) }
  }

  class Derived(b: Base) : Base by b


Functional Programming Features
-------------------------------

This category includes features related to functional programming and
the use of functions as first-class citizens. For example, use of lambdas,
declaration of higher-order functions, use of function types, etc.

Below you can find some functional programming features that
we encountered in the bug-revealing test cases.


Lambdas
^^^^^^^

The test case uses a lambda expression.

Example:

.. code-block:: kotlin

	fun test() {
	  val x = x: Int -> x
	}


Function Reference
^^^^^^^^^^^^^^^^^^

The test case involves a function reference.

Example:

.. code-block:: kotlin

  class A {
    fun m() = ""
  }

  fun test() {
    val x = A()
    x::m
  }


Function Type
^^^^^^^^^^^^^

The test case declares a parameter, field, variable whose type
is a function type.

Example:

.. code-block:: kotlin

  
  class A {
    fun m() = ""
  }

  fun test() {
    val x = A()
    val y: () => String = x::m
  }


SAM Type
^^^^^^^^

The test case declares a Single Abstract Method (SAM) interface
which is implemented by a lambda or function reference.

.. code-block:: java

  interface I {
    int m();
  }

  class Test {
    int m2(I x) {
      return x.m();
    }
    
    void test() {
      m2 { -> 1 };
    }
  }


ETA Expansion
^^^^^^^^^^^^^^

The test case involves the eta expansion technology (Scala only).

.. code-block:: scala

	object Test {
	  def m(x: Int) = x

	  def test() {
		val x = m _
	  }
	}


Parametric Polymorphism
-----------------------


This category includes features related to parametric polymorphism,
e.g., declaration of parameterized classes / functions, use of
parameterized types, etc.

Below you can find some features related to parametric polymorphism that
we encountered in the bug-revealing test cases.


Parameterized Class
^^^^^^^^^^^^^^^^^^^^

The test case declares a class that receives type parameters.

Example:

.. code-block:: kotlin

 class A<T>


Parameterized Type
^^^^^^^^^^^^^^^^^^^

The test case declares a field, parameter or variable
whose type is parameterized.

Example:

.. code-block:: kotlin

	class A<T>
	class B(val x: A<String>)


Parameterized Function
^^^^^^^^^^^^^^^^^^^^^^

The test case declares a function that receives type parameters.

Example:

.. code-block:: kotlin

	class A {
		fun <T> m(x: T) = x
	}


Bounded Type Parameters
^^^^^^^^^^^^^^^^^^^^^^^^

The test case defines a type parameter with a bound.

Example:

.. code-block:: kotlin

  class A<T: Number>

Declaration-Site Variance
^^^^^^^^^^^^^^^^^^^^^^^^^

The test case declares a type constructor with variant type parameters.

Example:

.. code-block:: kotlin

  class A<out T> // covariant type parameter

Use-Site Variance
^^^^^^^^^^^^^^^^^

The test cases uses a parameterized type with variant type arguments
(Kotlin, Groovy and Java only).

Example:

.. code-block:: kotlin

   class A<T>
   fun test() {
     val x: A<out Number> = A<Int>()
   }


Higher-Kinded Types
^^^^^^^^^^^^^^^^^^^

The test case declares a type constructor that receives
another type constructor as a type parameter (Scala only).

Example:

.. code-block:: scala

  class B[T]
  class A[B[_]]


Type Inference Features
-----------------------

This category includes features related to type inference.
For example, the input program declares a function whose return type
is omitted and inferred by the compiler.

Below we present some features related to type inference
that we encountered in the studied test cases.

Flow Typing
^^^^^^^^^^^

The test case makes use of implicit casts made by the compiler.

Example:

.. code-block:: kotlin

	fun test(x: Any) =
	  if (x is String)
		x // here the inferred type of x is String
	  else
		"val"

Type Argument Inference
^^^^^^^^^^^^^^^^^^^^^^^

The test case omits the type arguments of parameterized type.

Example:

.. code-block:: kotlin

  class A<T>
  fun bar(A<String>) {}
  fun test() {
    bar(A()) // omitted type arguments here
  }

Variable Type Inference
^^^^^^^^^^^^^^^^^^^^^^^

The test case declares a variable whose declared type is omitted.

Example:

.. code-block:: kotlin

	fun test() {
	  val x = "val"
	}

Parameter Type Inference
^^^^^^^^^^^^^^^^^^^^^^^^^

The test case declares a function or a lambda with parameters whose
declared types are omitted.

Example:

.. code-block:: kotlin

  fun bar(x: Int => Int) {}
  fun test() {
    bar(x -> x)
  }

Return Type Inference
^^^^^^^^^^^^^^^^^^^^^^

The test case declares a function whose return type is omitted.

Example:

.. code-block:: kotlin

  fun test() = "val"

Builder Inference
^^^^^^^^^^^^^^^^^

The test case involves builder-style type inference (Kotlin only).

Example:

.. code-block:: kotlin
  
  fun <T> sequence(@BuilderInference block: suspend SequenceScope<T>.() -> Unit): Sequence<T>
  fun test() {
    val result = sequence { yield("result") }
  }
