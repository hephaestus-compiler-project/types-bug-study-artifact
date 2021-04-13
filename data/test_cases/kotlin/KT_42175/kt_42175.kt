// !USE_EXPERIMENTAL: kotlin.ExperimentalStdlibApi

fun test(l: List<String>): String {
    val r = buildList {
        this += l[0]
    }
    return r[0]
}

fun box(): String =
    test(listOf("OK"))
