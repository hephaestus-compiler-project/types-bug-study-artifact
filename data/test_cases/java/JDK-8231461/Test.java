import java.util.function.*;
 
public class Test {
    public String foo(Object o) { return "foo"; }
    public static String foo(String o) { return "bar"; }

    public void test() {
        Function<String, String> f = Test::foo;
    }
}
