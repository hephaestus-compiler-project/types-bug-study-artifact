import java.util.List;
import java.util.function.Function;

public final class TestFail {
    public void build() {
        List<Function<String, Double>> list = transform(null, builder -> new Function<>() {
            public Double apply(String params) { return null; }
        });
    }

    static <F,T> List<T> transform(List<F> fromList, Function<? super F,? extends T> function) { return null; }
}
