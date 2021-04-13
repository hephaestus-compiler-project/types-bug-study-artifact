static <T extends Number> T id(T value) {
    value
}

// Narrower generic type: doesn't compile
static <T extends Integer> T id2(T value) {
    id(value)
}

// Narrower generic type: doesn't compile either
static <T extends Integer> T id3(T value) {
    A.<T>id(value)
}

// Fixed type: compiles
static Integer id4(Integer value) {
    id(value)
}
