object t {
  def f(x: Object) = 1
  def f(x: String*) = 2
}
t.f("") // returns 2, should be ambiguous.
