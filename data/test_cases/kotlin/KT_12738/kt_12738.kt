fun <T> get(t: T): () -> String {
    t.toString()         // ok, resolved to extension Any?.toString()
    return t::toString   // error, because erroneously resolved to member Any.toString()
}
