class Bar {
    fun invoke(x: Int): Int = x
}
class Foo {
    val get: Bar = Bar()
}
class Baz {
    public fun get(x: Int) : Int = x
}
 
// Compiles
fun test1 () {
    Foo().get(1)
}
 
// Compiles
fun test2() {
    Baz()[1]
}
 
// Does not compile
fun test3() {
    Foo()[1]
}
