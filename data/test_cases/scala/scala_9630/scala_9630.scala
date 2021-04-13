sealed trait Base
final case class Base_1(sameName: Some[Any]) extends Base
final case class Base_2(sameName: Nested) extends Base

sealed trait Nested
final case class Nested_1(x: Any) extends Nested
final case class Nested_2(y: Any) extends Nested

class Test {
  def test(b: Base): Unit = b match {
    case Base_1(Some(_)) =>
    case Base_2(Nested_1(_)) =>
    case Base_2(Nested_2(_)) =>
  }
}

