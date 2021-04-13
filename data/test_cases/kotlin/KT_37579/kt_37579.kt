class Foo<T>
class Bar<T>(val value: Foo<T>)

class Another {
    operator fun <T> Foo<T>.invoke(handler: () -> Unit) {}
}

fun Another.main(x: Bar<String>?) {
    x?.value {} // OK in OI, returns `Unit?`; unsafe call in NI
}
