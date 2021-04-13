class ImplicitThing

class Foo {
  def apply(x: Int)(implicit imp: ImplicitThing) = { println("read"); 123 }
  def update(x: Int, y: Int)(implicit imp: ImplicitThing) { println("updated") }
  
  // But the following alternative works!
  //def apply[T](x: T)(implicit imp: ImplicitThing) = { println("read"); 123 }
  //def update[T](x: T, y: T)(implicit imp: ImplicitThing) { println("updated") }
}

object TestCase extends App {
  implicit val imp = new ImplicitThing
  val foo = new Foo
  foo(3)               // works
  foo(3) = 4           // works
  foo(3) = foo(3) + 4  // works
  foo(3) += 4          // <-- compile error
}
