.. _bug_causes:

Bug Causes
==========

We classified the examined bugs
into categories based on their root cause.
To do so, we studied the fix of each bug
and identified which specific compiler's procedure was buggy.
From our manual inspection, we derived five categories
that include bugs sharing common root causes:

* *Type-related Bugs*
* *Semantic Analysis Bugs*
* *Resolution Bugs*
* *AST Transformation Bugs*
* *Bugs Related to Error Handling & Reporting*

In the following, we provide descriptions
and examples for every category.

Type-related Bugs
-----------------

To type check an input program,
a compiler consults the type system of the language,
which provides a set of rules of what are the language main types,
what operations on these types are valid,
how these types relate to each other,
and how they can be combined.
In this context, a compiler internally represents all types
and properties of the underlying type system
using specialized data structures.
Further, when typing an input program,
it applies abroad spectrum of operations to these data structures
based on the rules and design of the type system.
Corresponding examples include,
type variable substitutions, type constructor applications,
subtyping checks, type normalizations, and more.

We define a type-related bug when one of these type operations
is not implemented correctly.
Type-related bugs belong to one of the following scenarios:

* *Incorrect Type Inference & Type Variable Substitution*
* *Incorrect Type Transformation / Coersion*
* *Incorrect Type Comparison & Bound Computation*

Incorrect Type Inference & Type Variable Substitution
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In languages supporting type inference,
explicit types may be omitted in a program.
The compiler represents these omitted types with type variables,
which in turn, are replaced with concrete types at compile-time,
typically by solving a type constraint problem.
Many type-related bugs are caused by building a wrong constraint problem
(e.g., the constraint system contains excessive,
missing, or contradictory constraints),
or instantiating a type variable in a wrong way.
As a result, for a certain type variable,
the compiler infers a wrong type, or in many cases,
it is unable to infer a type at all.

Example 1:

`KT-10711 <https://youtrack.jetbrains.com/issue/KT-10711>`_

In this example, due to an incorrect handling of function references,
kotlinc constructs a constraint problem with incomplete constraints.
This makes it impossible for the compiler to solve the system
and find an optimal solution, leading to an
:ref:`unexpected compile-time error<Unexpected Compile-Time Error>`.


.. code-block:: kotlin

  class A<T>(val f: T)
  fun test() {
    listOf<String>().map(::A)
  }

Example 2:

`JDK-7041019 <https://bugs.openjdk.java.net/browse/JDK-7041019>`_

When dealing with an array type containing a type variable,
javac performs a wrong type variable substitution,
which causes a
:ref: `soundness bug<Unexpected Runtime Behavior>`.

.. code-block:: java

  interface A<E> {
    void m(E x);
  }

  interface B<Y> extends A<Y[]> { }

  class C implements B<Integer> {
    @Override
    void m(Integer[] x) { }

    static <T extends B<?>> void m2(T x) {
      //Boom! ClassCastException at runtime
      x.m(new String[]{"s"});
    }

    static void main(String[] args) {
      m2(new C());
    }
  }

Incorrect Type Transformation / Coercion
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Guided by certain rules, a compiler may transform
a certain type into another type for numerous reasons, e.g.,
type normalization, type erasure.
Similarly, we have the boxing and unboxing processes
where a value type becomes a reference type, and vice versa.
Diverse bugs in the implementation of these type transformations
cause many problems.

Example:

`KT-9639 <https://youtrack.jetbrains.com/issue/KT-9630>`_

This program defines a parameterized extension function
named :code:`m` instantiated by one type variable :code:`T`
that has two upper bounds: :code:`A` and :code:`B`.
The code later calls this function using a receiver of type :code:`C`.
When typing this program, kotlinc instantiates type variable :code:`T`
with the intersection type :code:`A & B`.
Since in Kotlin, intersection types are only used internally
for type inference purposes,
kotlinc needs to convert the intersection type :code:`A & B`
into a type that is representable in a program.
The problem in this example
is that kotlinc fails to convert type :code:`A & B` to type :code:`C`.
Consequently, kotlinc rejects the given code,
because it is unable to find the method :code:`m`
in a receiver of type :code:`C`,
even though this type has been extended with method :code:`m`.

.. code-block:: kotlin

  interface A
  interface B
  class C: A, B
  fun <T> T.m(): Unit where T: A, T: B { }
  fun main() {
    C().foo()
  }

Incorrect Type Comparison & Bound Computation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A compiler applies different kinds of comparisons between types,
which are underpinned by formal rules and relations of the type system.
For example, a compiler consults the subtyping rules of the type system
to check whether a value of type :math:`T_1`
is assignable to a variable of type :math:`T_2`.
Beyond that, a compiler implements a number of algorithms
dealing with type bounds,
such as computation of lowest upper bound and greatest lower bound.

Example:

`JDK-8039214 <https://bugs.openjdk.java.net/browse/JDK-8039214>`_

This example demonstrates a javac bug
caused by an incorrect type comparison.
While type checking the call on line 7,
javac checks whether the argument type :code:`C<?>`
is subtype of the expected type :code:`I<? extends X, X>`.
As part of this subtyping check, javac tests
if the type argument :code:`?` of type constructor :code:`C`
is contained in type argument :code:`? extends X` of type constructor :code:`I`.
This type argument comparison is guided by the containment relation
defined in the Java Language Specification(JLS).
Unfortunately, the implementation of javac
does not follow this containment relation to the letter.
Hence, it considers that :code:`C<?>` is not subtype of
:code:`I<? extends X, X>`.
This makes javac reject this well-formed program.

.. code-block:: java

  interface I<X1, X2> {}
  class C<T> implements T<T, T> {}

  public class Test {
    <X> void m(I<? extends X, X> arg) {}
    void test(C<?> arg) {
      m(arg);
    }
  }


Semantic Analysis Bugs
----------------------

Semantic analysis occupies an important space
in the design and implementation of compiler front-ends.
A compiler traverses the whole program
and analyzes each program node individually
(i.e., declaration, statement, and expression)
to type it and verify whether it is well-formed
based on the corresponding semantics.
A semantic analysis bug is a bug
where the compiler yields wrong analysis results
for a certain program node.
A semantic analysis bug occurs due to one of the following reasons:

* *Missing validation checks*
* *Incorrect analysis mechanics*

Missing Validation Checks
^^^^^^^^^^^^^^^^^^^^^^^^^

This sub-category of bugs
include cases where the compiler fails to perform a validation check
while analyzing a particular node.
This mainly leads to
:ref:`unexpected compile-time errors<Unexpected Compile-Time Error>`
because the compiler accepts a semantically invalid program
because of the missing check.
In addition to these false negatives,
later compiler phases may be impacted by these missing checks.
For example, assertion failures can arise,
when subsequent phases (e.g., back-end)
make assumptions about program properties,
which have been supposedly validated by previous stages.
Some indicative examples of validation checks include:
validating that a class does not inherit two methods with the same signature,
a non-abstract class does not contain abstract members,
a pattern match is exhaustive, a variable is initialized before use.

Example:

`Scala2-5878 <https://github.com/scala/bug/issues/5878>`_

This example demonstrates a semantic analysis bug
related to a missing validation check.
The program defines two value classes :code:`A` and :code:`B`
with a circular dependency issue,
as the parameter of :code:`A` refers to :code:`B`,
and the parameter of :code:`B` refers to :code:`A`.
This dependency problem, though,
is not detected by scalac, when checking the validity of these declarations.
As a result, scalac crashes at a later stage,
when it tries to unbox these value classes
based on the type of their parameter.
The developers of scalac fixed this bug
using an additional rule for detecting circular problems in value classes.

.. code-block:: scala

  case class A(x: B) extends AnyVal
  case class B(x: A) extends AnyVal


Incorrect Analysis Mechanics
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A common issue related to semantic analysis bugs
is incorrect analysis mechanics.
This sub-category contains bugs with root causes
that lie in the analysis mechanics
and design rather the implementation of type-related operations,
i.e., these bugs are specific to the compiler steps used for analyzing
and typing certain language constructs.
Incorrect analysis mechanics mostly causes
:ref:`compiler crashes<Internal Compiler Error>`
and :ref:`unexpected compile-time errors<Unexpected Compile-Time Error>`.

Example:

`Dotty-4487 <https://github.com/lampepfl/dotty/pull/4487>`_

In this bug, the compiler crashes,
when it types :code:`class A extends (Int => 1)`,
because Dotty incorrectly treats :code:`Int => 1` as a term
(i.e., function expression) instead of a type (i.e., function type).
Specifically, Dotty invokes the corresponding method for typing
:code:`Int => 1` as a function expression.
However, this method crashes
because the given node does not have the expected format.
Dotty developers fixed this bug by typing :code:`Int => 1` as a type.

.. code-block:: scala

  object 10 {
    def main(i1: Array[String]): Unit = {
      class i2
    }
    class i3(i4: => String) extends (i1 => (this 19)): Option[String, Int] => 1
  }


Resolution Bugs
---------------

One of a compiler's core data structures is that representing scope.
Scope is mainly used for associating identifier names with their definitions.
When a compiler encounters an identifier,
it examines the current scope and applies a set of rules to determine
which definition corresponds to the given name.
In OO languages where features, such as nested scopes,
overloading, or access modifiers, are prevalent,
name resolution is a complex and error-prone task.
A resolution bug is a bug where the compiler
is either unable to resolve an identifier name,
or the retrieved definition is not the right one.
A resolution bug is caused by one of the following scenarios:

* *there are correctnessissues in the implementation of resolution algorithms*
* *the compiler performs a wrong query*
* *the scope is an incorrect state (e.g., there are missing entries)*

The symptoms of resolution bugs are mainly
:ref:`unexpected compile-time errors<Unexpected Compile-Time Error>`
(when the compiler cannot resolve a given name or considers it as ambiguous)
or :ref:`unexpected runtime behaviors<Unexpected Runtime Behavior>`
(when resolution yields wrongdefinitions).


Example:

`JDK-7042566 <https://bugs.openjdk.java.net/browse/JDK-7042566>`_

In this example, for the method call at line 4,
javac finds out that there two applicable methods (see lines 6, 7).
In cases where for a given call,
there are more than one applicable methods,
javac chooses the most specific one according to the rules of JLS.
For our example, the method error defined at line 7 is the most specific one,
as its signature is less generic than
the signature of :code:`error` defined at line 6.
This is because the second argument of
:code:`error` at line 7 (:code:`Throwable`)
is more specific than the second argument of
:code:`error` (:code:`Object`) at line 6.
However, a bug in the way javac applies this applicability check
to methods containing a variable number of arguments
(e.g.,:code:`Object...`) makes the compiler treat these methods as ambiguous,
and finally reject the code.

.. code-block:: java

  class Test {
    void test() {
      Exception ex = null;
      error("error", ex);
    }
    void error(Object o, Object... p) { }
    void error(Object, Throwable t, Object... p) { }
  }


Bugs Related to Error Handling and Reporting
--------------------------------------------

When an error is found in a given source program,
modern compilers do not abort compilation.
Instead, they continue their operation to find more errors
and report them back to the developers.
In the context of type checking this is typically one
by assigning a special type (e.g., the top type) to erroneous expressions.
Compilers also strive to provide informative
and useful diagnostic messages
so that developers can easily locate
and fix the errors of their programs.
A bug related to error handling & reporting
is a bug where the compiler correctly identifies a program error,
but the implementation of the procedures
for handling and reporting this error does not produce the expected results.
All bugs of this category are related to
:ref:`crashes <Internal Compiler Error>`
and :ref:`wrong diagnostic messages <Misleading Report>`.


Example:

`KT-5511 <https://youtrack.jetbrains.com/issue/KT-5511>`_

This program triggers a bug with a misleading report
symptom, because the compiler produces two
contradictory error messages:

 * *error (2, 3): Modifier ’inner’ is not applicable to enum class"*
 * *error (2, 26): Expression is inaccessible from a nested class ‘C’, use ‘inner’ keyword to make the class inner”.*

This message suggests developers to take actions
that contradict with previously reported messages.

.. code-block:: kotlin
  :linenos:

  interface X<T> {
    inner enum class C : X<T>
  }


AST Transformation Bugs
-----------------------

The semantic analyses of a compiler
works on a program's abstract syntax tree (AST).
Before or after typing,
a compiler applies diverse transformations
and expressed in terms of simpler constructs.
For example, javac applies a transformation
that converts a foreach loop over a list of integers
:code:`for (Integer x: list)` into a loop of the form
:code:`for (Iterator<Integer> x = list.iterator(); x.hasNext();)`
An AST transformation bug is a bug where the compiler generates
a transformed program that is not equivalent with the original one,
something that invalidates subsequent analyses.

Example:

`Scala2-6714 <https://github.com/scala/bug/issues/6714>`_

This Scala 2 program defines a class :code:`B`
overriding two special methods named :code:`apply`,
and :code:`update` (lines 2–5).
The function :code:`apply` allows developers to treat an object as a function.
For example, a variable :code:`x` pointing to an object of class :code:`B`
can be used like :code:`x(10)`.
This is equivalent to :code:`x.apply(10)`.
Furthermore, the update method is used for updating the contents of an object.
For example, a variable :code:`x` of type :code:`B`
can be used in map-like assignment expressions
of the form :code:`x(10) = 5`.
This is equivalent to calling :code:`x.update(10, 5)`.
Notice that in our example,
the :code:`apply` method takes an implicit parameter of type :code:`A`.
This means that when calling this function,
this parameter may be omitted,
letting the compiler pass this argument automatically
by looking into the current scope for implicit definitions of type :code:`A`.
Before scalac types the expression on line 9, it "desugars" this assignment,
and expresses it in terms of method calls.
For example, :code:`b(3) += 4` becomes :code:`b.update(3, b.apply(3)(a) + 4)`.
However, due to a bug, scalac
ignores the implicit parameter list of :code:`apply`,
and therefore, it expands the assignment of line 9
as :code:`b.update(3, b.apply(3) + 4)`.
Consequently, the expanded method call does not type check,
and scalac rejects the program.

.. code-block:: scala

  class A
  class B {
    def apply(x: Int)(implicit a: A) = 1
    def update(x: Int, y: Int) { }
  }
  object Test {
    implicit val a = new A()
    val b = new B()
    b(3) += 4 // compile-time error here
  }
