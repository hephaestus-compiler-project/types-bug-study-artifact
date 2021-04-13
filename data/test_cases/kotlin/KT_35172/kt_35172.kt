fun <T> Any?.bar(): T = null as T

fun foo(a: String?): String? = run {
    a ?: a?.bar() // type mismatch (Required: String, Found: String?)
}
