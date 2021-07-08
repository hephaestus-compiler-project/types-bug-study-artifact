.. _errors:

Types of Errors
===============

To understand how bugs are introduced,
we manually studied every bug fix and
the discussion among developers
in the corresponding bug reports or commit messages.
We found that the bugs of our dataset are mainly introduced by logic errors,
algorithmic errors, design errors, or other programming errors.

In the following, we provide descriptions
and examples for every category.

Logic Errors
------------

Logic Errors stand for defects in logic, sequencing,
or branching of a procedure.
Logic Errors can further classified in the following categories.

* *Missing cases*
* *Extraneous computations*
* *Incorrect sequence of operations*
* *Wrong / insufficient parameters passed to a function*

Algorithmic Errors
------------------

Algorithmic errors are related to errors in the structure
and implementation of various algorithms employed by compilers
(e.g., inference of a type variable, resolution of a method).
Algorithmic errors arise either because the implementation of an algorithm
is wrong or because a wrong algorithm has been used.

Language Design Errors
----------------------

Language design errors express issues at a higher level.
They describe the cases where
although the compiler has the intended behavior
and is not buggy,
a program reveals that this behavior can lead to undesired results.
As a result, a re-design is essential for both the language and the compiler.

Programming Errors
------------------

Programming errors include declarations of a variable
with an incorrect data type, out-of-bounds array accesses,
accesses to null references, and unchecked exceptions.
