interface C {
    override fun toString(): String
}

open class A : C {
    override fun toString(): String = "A"
}

class B : C by A() // ABSTRACT_MEMBER_NOT_IMPLEMENTED
