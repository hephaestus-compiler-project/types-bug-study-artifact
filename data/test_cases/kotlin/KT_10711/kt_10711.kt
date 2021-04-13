class Wrapper<T>(val value: T)
​
fun test() {
    listOf<String>().map(::Wrapper) // "Not enough information to infer parameter T"
    listOf<String>().map { Wrapper(it) } // OK
}
