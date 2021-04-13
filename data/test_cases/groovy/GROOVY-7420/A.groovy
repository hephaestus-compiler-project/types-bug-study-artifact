class A {
    static String m(long p) {
        "primitive"
    }

    static String m(Long p) {
        "object"
    }
}

Long l = 42L
A.m(l)
