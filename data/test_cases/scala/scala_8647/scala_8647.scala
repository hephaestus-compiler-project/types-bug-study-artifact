final class Two[A, B]()

final class Bla[A]

object Test {

  type Foo[X] = X match
    case Two[Bla[_], _] =>
      String
    case Two[String, _] =>
      Int

  def test: Foo[Two[String, String]] = 1
}
