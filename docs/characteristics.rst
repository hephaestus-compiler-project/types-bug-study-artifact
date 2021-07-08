.. _characteristics:

Test Case Characteristics
=========================

By manually investigating the accompanying
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
* *Type System-Related Features*
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


Type System-Related Features
--------------------

This category includes features associated with the type system of
the languages. For example, subtyping, intersection types,
dependent types, type projections, etc.

Below you can find some type system-related features that we encountered
in the bug-revealing test cases.


Subtyping
^^^^^^^^^

The test case uses types for which the subtyping relation holds.

Example:

.. code-block:: java

  class A {}
  class B extends A {}

  A x = new B() // here we have subtyping


Primitive Types
^^^^^^^^^^^^^^^

The test case declares a variable/parameter whose type is primitive
(Java and Groovy only).

Example:

.. code-block:: java

  int x = 5;


Wildcard Types
^^^^^^^^^^^^^^

The test case contains a parameterized type that comes from the
application of a type constructor with a wildcard type, e.g. A<?>.

Example:

.. code-block:: kotlin

  public static void add(List<? extends Number> list) {}


Intersection Types
^^^^^^^^^^^^^^^^^^

The test case makes use of intersection types (Scala only).

Example:

.. code-block:: java

  interface A { }
  interface B { }

  public static <T extends A & B> void foo() { }


Dependent Type
^^^^^^^^^^^^^^

The test case declares a variable/parameter whose type is a dependent type
(Scala only).

Example:

.. code-block:: scala

  trait DepValue{
    type V
    val value: V
  }

  def magic(that: DepValue): that.V = that.value


Type Definition / Member
^^^^^^^^^^^^^^^^^^^^^^^^

Test case declares a Type Member (Scala only).

Example:

.. code-block:: scala

  class Blah {
    type Member
  }


Nothing
^^^^^^^

The test case handles the special type 'Nothing' (Scala, Kotlin only).


Example:

.. code-block:: scala

  val variable: Nothing? = null


Algebraic Data Type
^^^^^^^^^^^^^^^^^^^

The test contains algebraic data types (Scala only).


Example:

.. code-block:: scala

  sealed trait Bool
  case object True extends Bool
  case object False extends Bool


Type Lambdas
^^^^^^^^^^^^

The test case contains a type lambda expression (Scala only).

Example:

.. code-block:: scala

  [X, Y] =>> Map[Y, X]

For instance, the type above defines a binary type constructor,
which maps arguments :code:`X` and :code:`Y` to :code:`Map[Y, X]`.


Type Projection
^^^^^^^^^^^^^^^

The test case contains type projections (Scala only).


Example:

.. code-block:: scala

  class Foo {
    class Bar
  }
  val foo1 = new Foo
  val bar1: foo1.Bar = new foo1.Bar
  val foo2 = new Foo
  val bar2: foo2.Bar = new foo2.Bar
  val bar: Foo#Bar = if (???) bar1 else bar2


Opaque Type
^^^^^^^^^^^

The test case defines opaque type alias (Scala only).


Example:

.. code-block:: scala

  opaque type Logarithm = Double


Union Type
^^^^^^^^^^

The test case makes use of union types (Scala only).


Example:

.. code-block:: scala

  case class UserName(name: String)
  case class Password(hash: Hash)

  def help(id: UserName | Password) =
    val user = id match
      case UserName(name) => lookupName(name)
      case Password(hash) => lookupPassword(hash)
    ...


Mixins
^^^^^^

The test case uses a mixin type (Scala only).

Example:

.. code-block:: scala

  abstract class A {
    val message: String
  }
  class B extends A {
    val message = "I'm an instance of class B"
  }
  trait C extends A {
    def loudMessage = message.toUpperCase()
  }
  class D extends B with C // Class D has a superclass B and a mixin C.


Match Type
^^^^^^^^^^

The test case performs pattern matching on types (Scala only).


Example:

`Dotty Example http://dotty.epfl.ch/docs/reference/new-types/match-types.html`_


Nullable Type
^^^^^^^^^^^^^

The test case uses nullable types (Kotlin only).


Example:

.. code-block:: kotlin

  var b: String? = "abc"
  b = null


Standard Library
----------------

Function API
^^^^^^^^^^^^

The test case uses the function API from the standard library of Java.


Refelection API
^^^^^^^^^^^^^^^

The test case us the reflection API.

Example:

.. code-block:: java

  class A { }
  val x = new A()
  x.getClass()


Collection API
^^^^^^^^^^^^^^

The test case uses the collection API (e.g., it uses list types, it
creates sets, and more).


Stream API
^^^^^^^^^^

The test case uses the Stream API from the standard library of Java.

Coroutines API
^^^^^^^^^^^^^^

The test case uses the Coroutines API (Kotlin only).


Delegation API
^^^^^^^^^^^^^^

The test case uses the Delegation API from the standard library of Groovy.


Other
-----

Type Annotations
^^^^^^^^^^^^^^^^

The test case contains annotations.


Java Interoperability
^^^^^^^^^^^^^^^^^^^^^

The test case is written in a language other than Java, but uses part of
code written in Java (e.g., a library, imports a Java class, uses the
standard library of Java, etc.)



Implicits
^^^^^^^^^

The test case uses implicits (Scala only).

Example:

.. code-block:: scala

  class Prefixer(val prefix: String)
  def addPrefix(s: String)(implicit p: Prefixer) = p.prefix + s
  implicit val myImplicitPrefixer = new Prefixer("***")
  addPrefix("abc")


Erased Parameter
^^^^^^^^^^^^^^^^

The test case contains erased parameters (Scala only).


Example:

.. code-block:: scala

  def methodWithErasedEv(erased ev: Ev): Int = 42


Call by Name
^^^^^^^^^^^^

The test case contains call-by-name arguments (Scala only).

Example:

.. code-block:: scala

  def calculate(input: => Int) = input * 37


Default Initializer
^^^^^^^^^^^^^^^^^^^

The test case contains a default initializer (Scala only).

Example:

.. code-block:: scala

  class Socket(var timeout: Int = 2000, var linger: Int = 3000) { }


Option Type
^^^^^^^^^^^

The test case declares a variable, parameter or field
with an option type (Scala only).

Example:

.. code-block:: scala

  object Test {
    def test(x: Option[String]) = x match {
        case None => ???
        case Some(str) => ???
    } 
  }


Pattern Matching
^^^^^^^^^^^^^^^^

The test case contains pattern matching (Scala only).

Example:

.. code-block:: scala

  val x: Int = Random.nextInt(10)

  x match {
    case 0 => "zero"
    case 1 => "one"
    case 2 => "two"
    case _ => "other"
  }


Inline
^^^^^^

The test case uses the inline keyword (Scala and Kotlin only).


Example:

.. code-block:: kotlin

  inline fun <T> lock(lock: Lock, body: () -> T): T { ... }


Named Arguments
^^^^^^^^^^^^^^^

The test case contains a function that takes named arguments
(Kotlin, Scala, and Groovy only).

Example:

.. code-block:: groovy

  String foo(String x, String y = "foo")


Extension Function / Property
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The test case defines an extension function or property (Kotlin only).

Example:

.. code-block:: kotlin

  fun MutableList<Int>.swap(index1: Int, index2: Int) { }


Elvis Operator
^^^^^^^^^^^^^^

The test case contains an elvis expression (Kotlin, Groovy only).

Example:

.. code-block:: kotlin

  val list = mutableList ?: mutableListOf()


Null Assertion
^^^^^^^^^^^^^^

The test case contains a null assertion expression (Kotlin only).

Example:

.. code-block:: kotlin

  val answer = "42"
  answer!!.toInt()


Safe Navigation Operator
^^^^^^^^^^^^^^^^^^^^^^^^

The test case contains an safe navigation operator (Kotlin, Groovy only).


Example:

.. code-block:: kotlin

  val name = article?.author?.name


With
^^^^

The test case performs multiple assignments through the with pattern
(Groovy only).


Example:

.. code-block:: groovy

  Foo foo = new Foo()
  foo.with {
      name = 'Foo'
      age = 2
  }


Template String
^^^^^^^^^^^^^^^

The test case contains a template sting (Groovy, Kotlin, Scala only).

Example:

.. code-block:: groovy

  String greet(String otherPerson) {
    "Hello ${otherPerson}"
  }
