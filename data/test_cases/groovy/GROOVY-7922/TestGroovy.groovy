interface FooA {}
interface FooB {}
class FooAB implements FooA, FooB {}
class TestGroovy {
    static void test() { println new TestGroovy().foo(new FooAB()) }
    def foo(FooB x) { 43 }
    def foo(FooA x) { 42 }
}

TestGroovy.test()
