@CompileStatic
class Groovy9881 {

    def doReplace() {
        new Value(123)
            .replace(() -> "foo")

        new Value(123)
            .replace((Integer v) -> "bar")
    }

    static class Value<V> {
        final V val

        Value(V v) {
            this.val = v
        }

        <T> Value<T> replace(Supplier<T> supplier) {
            new Value<>(supplier.get())
        }

        <T> Value<T> replace(Function<? super V, ? extends T> function) {
            new Value(function.apply(val))
        }
    }
}
