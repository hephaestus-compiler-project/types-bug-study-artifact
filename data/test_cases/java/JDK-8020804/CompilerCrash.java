import java.util.*;

interface Supplier<D> {
   D make();
}

class CompilerCrash {
    void m(Object o) { }
    void m(char[] c) { }

    <C extends Collection<?>> C g(Supplier<C> sc) { return null; }


    // crashes when toString() is omitted
    void test() {
        m(g(LinkedList<Double>::new));
    }
}
