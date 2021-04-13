class Foo {
    def bar() { 2 }

    static class Baz {
        def doBar() {
            bar()
        }
    }
}
new Foo.Baz().doBar()
