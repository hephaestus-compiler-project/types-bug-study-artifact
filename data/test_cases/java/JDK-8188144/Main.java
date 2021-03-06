import java.util.function.BiFunction;

public class Main {
    public static void main(String[] args1) {
        BiFunction<String, String, String> format = String::format;
        System.out.println(format.apply("foo %s", "bar")); // yields "foo bar" in java8, yields "bar" in java9

        BiFunction<String, Object, String> java9format = String::format;
        System.out.println(java9format.apply("foo %s", "bar")); // yields "foo bar" in java9
    }
}