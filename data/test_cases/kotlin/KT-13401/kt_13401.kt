interface Rec<T: Rec<T>> {
    fun t(): T
}
interface Super {
    fun foo(p: Rec<*>) = p.t()
}
