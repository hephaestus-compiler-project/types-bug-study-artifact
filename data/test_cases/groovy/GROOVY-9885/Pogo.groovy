static class HasString {
    String value
}

void foo(String a, String b, String c) {
    new HasString(
        value: (a ?: "$b $c")
    )
}
