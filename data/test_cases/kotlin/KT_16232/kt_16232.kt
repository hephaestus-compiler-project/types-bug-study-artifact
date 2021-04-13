class A {
    val x = "OK"

    inner class B {
        object Q { // must be prohibited
            fun foo() = x
        }
    }
}

fun main(args: Array<String>) {
    println(A.B.Q.foo())
}
