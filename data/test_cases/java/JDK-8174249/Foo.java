import java.util.ArrayList;
import java.util.Collection;

public class Foo {
    static <T> T foo(Class<T> c, Collection<? super T> baz) {
        return null;
    }

    static void bar(String c) {

    }

    @SuppressWarnings("unchecked")
    public static void main(String[] args) {
        // this works
        bar(foo(String.class, new ArrayList<String>()));

        // this works with a warning
        String s = foo(String.class, new ArrayList());
        bar(s);

        // this causes an error on JDK9
        bar(foo(String.class, new ArrayList()));
    }
}
