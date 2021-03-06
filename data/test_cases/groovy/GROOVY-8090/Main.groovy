import static java.util.Arrays.asList
class Main {
    final <T> Iterable<T> foo(T instance) { asList(instance) }
    // next line fails with: [Static type checking] - Cannot call <T> java.util.Arrays#asList(T[]) with arguments [U]
    final <U> Iterable<U> bar(U instance) { asList(instance) }
    final Iterable<String> baz(String instance) { asList(instance) }
}

new Main().with {
    assert foo('A') + bar('B') + baz('C') == ['A', 'B', 'C']
}
