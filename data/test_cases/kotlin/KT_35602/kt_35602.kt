interface Self<E : Self<E>> {
    val x: E
}
fun foo(): Self<*>? = TODO()
fun bar(): Self<*> = TODO()
fun main(args: Array<String>) {
    bar().x.x.x.x.x.x.x.x.x.x.x.x.x // OK
    foo()!!.x.x.x.x.x.x // OK
    foo()!!.x.x.x.x.x.x.x // unresolved last "x" in NI
}
