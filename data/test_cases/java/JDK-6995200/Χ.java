class X {
    public static <T> T getValue() {
        return null;
    }

    public void testGenerics(Comparable<String> s) {
        int i = getValue();
    }
}
