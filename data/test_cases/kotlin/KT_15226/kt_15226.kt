class Fail : Base {
    override fun getValue() = "Fail"
}

fun box(): String {
    val z = object : Base by Fail() {
        override fun getValue() = "OK"
    }
    return z.test()
}
