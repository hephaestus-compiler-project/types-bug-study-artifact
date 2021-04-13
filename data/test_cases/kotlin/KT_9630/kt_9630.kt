interface Foo<T>
interface Bar<T>

class Baz<T> : Foo<T>, Bar<T>

fun <T, FooBar : Foo<T>> FooBar.bip() where FooBar: Bar<T> {}

fun main(args: Array<String>) {
    val baz = Baz<String>()
    baz.bip() // Doesn't work
}
