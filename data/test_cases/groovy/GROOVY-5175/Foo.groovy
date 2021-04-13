class Foo {
    def say() {
        methodWithArrayParam(null) // STC Error
    }
    def methodWithArrayParam(String[] s) {

    }
}
