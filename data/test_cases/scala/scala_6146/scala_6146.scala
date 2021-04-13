trait BS[T, S <: BS[T, S]]
trait IS extends BS[Int, IS]

sealed trait BSElem[T, S <: BS[T, S]]

object BSElem {
  implicit val intStreamShape: BSElem[Int, IS] = ???
}
class Ops[A] {
  def asJavaSeqStream[S <: BS[A, S]](implicit s: BSElem[A, S]): S = ???
}
