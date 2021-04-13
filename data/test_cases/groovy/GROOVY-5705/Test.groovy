class Test {
    Closure c = { it }

    void test() {
        c("123")
    }
}

new Test().test()
