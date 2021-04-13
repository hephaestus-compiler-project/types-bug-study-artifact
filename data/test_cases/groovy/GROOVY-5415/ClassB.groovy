class ClassB {
    void bar() {
        def ClassA<Long> a = new ClassA<Long>();
        a.foo(this.getClass());
    }
}
