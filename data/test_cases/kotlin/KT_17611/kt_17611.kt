fun foo(name: String) {
    object {
        fun bar(name: String) {}  // Name shadowed: "name"
    }
}
