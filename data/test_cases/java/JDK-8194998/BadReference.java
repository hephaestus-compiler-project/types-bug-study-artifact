class BadReference {
    void foo() {
        // ::test is not a member of any subclass of I as it is private
        Runnable test2 = ((new I() {}))::test;
    }

    interface I {
        private void test() {}
    }
}