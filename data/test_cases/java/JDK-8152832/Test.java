import java.util.function.*;
import java.util.stream.*;
import java.util.*;

public class Test {
    interface MyStream<T> extends Stream<T> {
        public <U> List<U> toFlatList(Function<? super T, ? extends Collection<U>> mapper);
    }

    static class MyStreamSupplier<T> {
        public MyStream<T> get() {return null;}
    }

    public static <T> void myStream(Supplier<Stream<T>> base, Consumer<MyStreamSupplier<T>> consumer) {
    }

    public static void assertEquals(Object expected, Object actual) { }

    public void test() {
        List<List<String>> strings = Arrays.asList();
        List<String> expectedList = Arrays.asList();
        myStream(strings::stream, supplier -> {
            assertEquals(expectedList, supplier.get().toFlatList(Function.identity()));
        });
    }
}