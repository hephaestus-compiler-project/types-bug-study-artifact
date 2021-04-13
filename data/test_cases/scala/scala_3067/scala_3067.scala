import scala.collection.generic.CanBuildFrom

class Test {
  implicitly[CanBuildFrom[List[_], Int, List[Int]]]

  class Foo[T](x: T)
  implicit object Bar extends Foo(
    implicitly[CanBuildFrom[List[_], Int, List[Int]]]
  )
}
