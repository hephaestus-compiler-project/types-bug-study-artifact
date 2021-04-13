class Mylist implements List<Object> {
    int size() { }
    boolean isEmpty() {}
    boolean contains(final Object o) {}
    Iterator iterator() {[].iterator()}
    Object[] toArray() {}
    Object[] toArray(final Object[] a) {}
    boolean add(final Object e) {}
    boolean remove(final Object o) {}
    boolean containsAll(final Collection<?> c) {}
    boolean addAll(final Collection c) {}
    boolean addAll(final int index, final Collection c) {}
    boolean removeAll(final Collection<?> c) {}
    boolean retainAll(final Collection<?> c) {}
    void clear() {}
    Object get(final int index) {}
    Object set(final int index, final Object element) {}
    void add(final int index, final Object element) {}
    Object remove(final int index) {}
    int indexOf(final Object o) {}
    int lastIndexOf(final Object o) {}
    ListIterator listIterator() {}
    ListIterator listIterator(final int index) {}
    List subList(final int fromIndex, final int toIndex) {}
}
def whatthe(Mylist a) {
   a.find { true }
}
