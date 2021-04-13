class JDK8148354 {
    interface I {}
    interface J { void foo(); }

    <T extends Object & I & J> void consume(T arg) { }

    public void test() {
        consume(System::gc);
    }
}
