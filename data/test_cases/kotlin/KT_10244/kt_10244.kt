open class B
interface A
interface C

fun foo(b: B) = if (b is A && b is C) b else null
