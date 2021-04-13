import java.util.List;
import java.util.ArrayList;
import java.util.Collection;

public class JavaClass {

    public static class Container<T> {
    }

    public static class StringContainer extends Container<String> {
    }

    public static <T> List<T> unwrap(Collection<? extends Container<T>> list) {
        return null;
    }

    public static void main(String[] args) {
        final List<StringContainer> containers = new ArrayList<>();
        final List<String> strings = unwrap(containers);
    }
}
