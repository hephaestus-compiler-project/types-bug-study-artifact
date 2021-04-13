import kotlin.reflect.KProperty

// Always returns null
class NullReturningDelegate {
    operator fun getValue(thisRef: Any?, property: KProperty<*>): Any? = null
    operator fun setValue(thisRef: Any?, property: KProperty<*>, value: Any?) {}
}

// Alternates Int and String as return types
class AlternatingDelegate {
    var counter: Int = 0
    operator fun getValue(thisRef: Any?, property: KProperty<*>): Any? =
        if (counter++ % 2 == 0) 42 else ""
}

fun failsWithNullPointerException() {
    var alwaysNull: Any? by NullReturningDelegate()

    alwaysNull = "" // Provoke unsound smartcast

    alwaysNull.hashCode() // Smartcasted to not-null
}

fun failsWithClassCastException() {
    val sometimesNotInt: Any? by AlternatingDelegate()

    if (sometimesNotInt is Int) {
        sometimesNotInt.inc() // Smartcasted to Int
    }
}
