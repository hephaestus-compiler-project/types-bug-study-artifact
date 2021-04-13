class A {}
class B {
    Object m(Object[] args) {
        new Object()
    }
}
class C extends B {
    A m(Object[] args) {
        new A()
    }
}
C c = new C()
A a = c.m()
