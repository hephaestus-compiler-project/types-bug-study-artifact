class A {}
class B extends A { def bbb() {} }

def fooLocalAssignment() {
    A a = new B()
    a.bbb()
}

def fooParameterAssignment(A a) {
    a = new B()
    a.bbb() // Cannot find matching method A#bbb()
}
