//module A
class Foo<out T>(
        val t: T
) {
    typealias Bar = (T) -> Unit

    fun baz(b: Bar) = b(t)
}
