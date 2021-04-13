open class A {
    var a = 1
}

class B(override val a: Int) : A() {
}
