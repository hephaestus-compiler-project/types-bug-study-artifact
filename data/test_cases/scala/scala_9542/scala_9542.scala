object O {
  trait T // does not crash if T is top level.

  class VC(val self: Any) extends AnyVal {
    def extMethod(f: F1[T, Any]) = ()
  }
}
trait F1[A, B]
