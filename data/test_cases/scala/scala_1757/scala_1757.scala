case class B[T](b: List[Int]) {
  var s: B[Int] = _
  s copy ()
}
