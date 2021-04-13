interface Int {
    void main();
}

class MyInt implements Int {
    public void main() {
        System.out.println("Hello, world!");
    }
}

class BasicUnit {
    static <T extends Int> T factory(Class<T> c) throws Throwable {
        return c.newInstance();
    }
    public static void main(String[] args) throws Throwable {
        factory(Class.forName("MyInt").asSubclass(Int.class)).main();
    }
}
