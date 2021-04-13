trait Foo { self =>
  type M
  def apply(prog: (h: self.type) => h.M): M = prog(this)
}
