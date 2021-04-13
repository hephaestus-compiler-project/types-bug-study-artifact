import java.util.function.*;

public class TimingOfMReferenceCheckingTest01 {
    <Z> void g(Consumer<Z> fzr, Z z) {}

    void test(boolean cond) {
       g(cond ? this::m : this::m, "");
    }

    void m(String s) {}
    void m(Integer i) {}
}