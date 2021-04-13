class X[A](a: A)
object Test {
  def local = {
    implicit object X extends X("".reverse)
    implicitly[X[String]]
  }
}
