fun main(x: Map<String, Pair<String, String>>) {
    x + (x ?: emptyMap())
}
