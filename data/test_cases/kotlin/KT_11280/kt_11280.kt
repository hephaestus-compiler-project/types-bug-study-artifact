class Q {
    override fun equals(other: Any?) = true

    fun f(){}
}

fun foo(q: Any) {
    val someQ = Q()
    if (someQ == q) {
        q.f() // ClassCastException: java.lang.Integer cannot be cast to Q
    }
}

fun main(args: Array<String>){
    foo(1)
}
