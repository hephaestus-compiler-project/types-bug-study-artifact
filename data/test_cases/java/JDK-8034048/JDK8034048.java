public interface Null {
    static<T> void functional(T... input) {
        java.util.function.Consumer<T> c = Null::functional;
    }
}