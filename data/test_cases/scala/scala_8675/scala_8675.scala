class A(s: String) {
  def foo(x: A) = x
	
  def test {
    val a = Array[A]()
    for (i <- 0 to 0) {
      a(i) = a(i).foo(new A(i))
    }
  }
}
