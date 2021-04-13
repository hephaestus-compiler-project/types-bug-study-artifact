interface A {
    String getName();
}

interface B extends A {
    void foo();
}

class C {
    String name
    void bar(B b)
    {
        b.foo()
        name = b.name
    }
}
new C()
