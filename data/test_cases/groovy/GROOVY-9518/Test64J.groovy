class C {
    C(String s, Comparable<List<Integer>> c) { }
}
new C('blah', { list -> list.get(0) })
