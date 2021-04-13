open class ZException<T>(val p: T) : Exception() {
}

fun main(args: Array<String>) {
    try {
        throw ZException(11)
    } catch (e: ZException<String>) {
        val s: String = e.p
    }
}
