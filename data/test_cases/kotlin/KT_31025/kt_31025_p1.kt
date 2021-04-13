public interface JSam<T, R> {
    R apply(T t);
}

class Inv<T> {
    public final <R> Inv<R> map(Function<? super T, ? extends R> mapper) {
        return null;
    }
}
