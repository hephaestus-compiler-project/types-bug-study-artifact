fun foo<T : Any, S : T>() where S : Any? {
    val s : S = null
    val t : T = s
    val a : Any = t
    if (a == null) { // Warning:(5, 9) Kotlin: Condition 'a == null' is always 'false'
        println("O RLY?")
    }
}

fun main(args : Array<String>) {
    foo<Any, Any>()
}
