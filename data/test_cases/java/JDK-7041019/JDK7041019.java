class JDK7034511 {
    interface A<T> {
        void foo(T x);
    }

    interface B<T> extends A<T[]> { }
    static abstract class C implements B<Integer> {
        <T extends B<?>> void test(T x, String[] ss) {
            x.foo(ss);
        }
    }
}
