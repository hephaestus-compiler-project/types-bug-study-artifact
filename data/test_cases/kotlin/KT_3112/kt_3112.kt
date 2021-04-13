class C<T> {
    class Inner
    fun f(p: C.Inner) {} // Should be an error: C requires type arguments
}
