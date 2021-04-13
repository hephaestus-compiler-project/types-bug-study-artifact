class D
class C[+T](x: T)

class Foo() {
  val status: Int = 0
}

object Main {
  implicit class RichC[T](c: C[T]) {
    def await(implicit d: D = ???): T = ???
      // it's critical that the default is selected on the call below
      // it works if there is an implicit in scope for `d`
  }

  def test1: Int = {
    val foo = new C(new Foo()).await
    foo.status
  }

  val test2 = new C(new Foo()).await.status
}
