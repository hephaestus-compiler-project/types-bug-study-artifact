interface A1{}
interface A2 extends A1{}

class C1 implements A1{}
class C2 extends C1 implements A2 {}

def m(A2 a2) {
       C1 c1 = (C1) a2 // There is error here now: Inconvertible types: cannot cast A2 to C1
}
