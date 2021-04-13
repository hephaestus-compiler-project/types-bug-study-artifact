class Test {
    <T extends Comparable<? super T>> Comparator<List<T>> comparator() { return null; }
    static <T extends Comparable<? super T>> void f() {
       Comparator<List<T>> comparator = comparator(); // [*]
    }
 }