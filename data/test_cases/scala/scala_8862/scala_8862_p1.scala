package x

class Oops

abstract class ns2super[A] {
  def x: A
  implicit def oops: A = x
  implicit def oopso: Option[A] = None
}

package object nodescala2 extends ns2super[Oops] {
  override def x = new Oops
}
