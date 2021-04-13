fun <T : Exception> foo() : T {
    try {
        throw Exception()
    }
    catch(x : T) { // Actually it catches Exception, that is not typesafe
        return x
    }
}

fun main(args: Array<String>) {
    val x = foo<ArithmeticException> ()
}
