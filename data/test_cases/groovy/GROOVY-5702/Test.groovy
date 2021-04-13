interface MyCloseable {
    void close()
}

interface OtherCloseable extends MyCloseable {
    void close()
}

class MyCloseableChannel implements OtherCloseable {}

class Test {
    static void test() {
        def mc = new MyCloseableChannel()
        mc.close()
    }
}

Test.test()
