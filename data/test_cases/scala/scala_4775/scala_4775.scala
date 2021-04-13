class A {
  def f[T](x: T): T = x
  def f[T](x: T, xs: T*): T = x
  
  f(5)
  
  // but this works:
  def g(x: Int): Int = x
  def g(x: Int, xs: Int*): Int = x

  g(5)
}
