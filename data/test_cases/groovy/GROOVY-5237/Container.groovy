class Container<T> {
    private T initialValue
    Container(T initialValue) { this.initialValue = initialValue }
    T get() { initialValue }
}
