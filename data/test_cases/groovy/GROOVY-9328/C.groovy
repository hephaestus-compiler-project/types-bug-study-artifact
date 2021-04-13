class C {

    private C() {}
    private privateMethod() {}

    def anonymousUsage() {
        new Runnable() {
            @Override
            void run() {
                privateMethod()
                new C()
            }
        }
    }
}
