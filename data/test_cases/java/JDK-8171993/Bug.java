public class Bug<T> {
    public T invoke(Object... args) {
        return null;
    }
    public static <T extends String> void test() { // works with <T> alone.
        Bug<T> bug = new Bug<>();
        java.util.function.Function<String, T> b = bug::invoke; // compile error, but works with (args) -> bug.invoke(args);
    }
}