interface In<in E> 
open class A : In<A>
open class B : In<B>

fun <T> select(x: T, y: T) = x

fun foo2() = select(A(), B()) // No error, but return type 'In<A & B>' contains intersection
