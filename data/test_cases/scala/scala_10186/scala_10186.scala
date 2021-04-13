trait Foo {
  type A
  type F[_ <: A]
}

object Test {
  def noop[A, F[_ <: A]]: Unit = ()

  def f(foo: Foo): Unit = {
    noop[foo.A, foo.F] // does not compile
  }
}
