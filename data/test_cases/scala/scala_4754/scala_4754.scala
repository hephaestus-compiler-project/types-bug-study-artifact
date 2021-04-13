object Foo {
  private final val C = 1
}

class Foo {
  import Foo._
  inline def foo(x: Int): Boolean = x == C
}
