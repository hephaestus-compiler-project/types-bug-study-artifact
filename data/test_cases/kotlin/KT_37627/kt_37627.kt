fun foo(x: Int) {
    val x = if (true) { // OI: Map<String, () → Int>?, NI: Nothing?, error
        "" to { x }
    } else { null }
}
