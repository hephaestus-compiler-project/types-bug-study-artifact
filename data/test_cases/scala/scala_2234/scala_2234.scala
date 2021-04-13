type Dummy[A] = A
def m(d: Dummy[String]) = ()
def m(d: Dummy[Int]) = ()
