import java.util.stream.Collectors
import java.util.stream.Stream

public class Test1 {
    public static void main(String[] args) {
        p();
    }

    public static void p() {
        assert 13 == Stream.of(1, 2, 3).reduce(7, {r, e -> r + e});
    }
}
