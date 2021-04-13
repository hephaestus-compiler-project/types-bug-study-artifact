class A<T> {
    val children = mutableListOf<B<T>>()
}
class B<T>
class C {
    var a: A<*>? = null
    var b: B<*>? = null
        set(value) {
            if (value != null) {
                val a = a
                require(a != null && value in a.children)
            }
            field = value
        }
}
