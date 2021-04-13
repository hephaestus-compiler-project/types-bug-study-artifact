class Inv<V>

fun <K> select(x: K, y: K): K = x
fun <T> generic(x: Inv<T>) {}

fun bar(a: Inv<out Any>, b: Inv<out Any>) {
    generic(select(a, b)) // error in NI, ok in OI

    // but:
    val x = select(a, b)
    generic(x) // OK everywhere, because of local inference
}
