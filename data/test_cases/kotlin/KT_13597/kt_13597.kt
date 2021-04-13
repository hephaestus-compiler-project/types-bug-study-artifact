class Test {
    val a: String

    constructor() {
        val t = object {
            fun some() {
                a = "12" // OK for the compiler
            }
        }

        a = "2"
        t.some()
    }
}

fun main(args: Array<String>) {
    Test() // java.lang.IllegalAccessError: tried to access field Test.a from class Test$t$1
}
